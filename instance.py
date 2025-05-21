from pyscipopt import Model
from itertools import combinations


class Instance:
    def __init__(self, M):
        self.processing_times = M   # An m x n tuple of tuples with string values '0', 's', 'b'
        self.n_jobs = len(M[0])
        self.n_machines = len(M)

    def opt_LP(self):
        """
        Do a binary search to find the smallest integer for which is_feasible(T) is true.
        The initial guesses are as follows:
            l = highest processing time for any job - 1
            r = sum of all processing times
        We maintain the invariant that LB is in (l, r].
        """
        right = sum(sum(int(self.processing_times[i][j]) for j in range(self.n_jobs)) for i in range(self.n_machines))
        left = max(max(int(self.processing_times[i][j]) for j in range(self.n_jobs)) for i in range(self.n_machines))-1
        while right - left > 1:
            m = (left + right)//2
            is_feasible = self.is_feasible(m)
            if is_feasible:
                right = m
            else:
                left = m

        return right

    def is_feasible(self, T):
        """
        :param T: integer
        :return: True if LP(T) is feasible, otherwise False
        """
        model = Model('Restricted assignment with 2 processing times')
        model.hideOutput()

        # Determining valid configurations (with makespan at most T) for each machine in the form of a dict
        # Values are lists of tuples, one tuple for each valid configuration
        configs = {i: [c for length in range(1, self.n_jobs) for c in combinations([j for j in range(self.n_jobs) if self.processing_times[i][j] != '0'], length) if sum(int(self.processing_times[i][j]) for j in c) <= T] for i in range(self.n_machines)}

        # Decision variables
        x = {}
        for i in configs.keys():
            for c in configs[i]:
                x[i, c] = model.addVar(vtype="C", name=f"x({i},{c})", lb=0.0)

        # Each machine can allocate at most 1 config
        for i in range(self.n_machines):
            if len(configs[i]) != 0:
                model.addCons(sum(x[i, c] for c in configs[i]) <= 1)

        # Each job gets allocated at least once
        for j in range(self.n_jobs):
            model.addCons(sum(sum(x[i, c] for c in configs[i] if j in c) for i in range(self.n_machines)) >= 1)

        model.optimize()
        if model.getStatus() == 'optimal':
            return True
        return False

    def opt_IP(self):
        model = Model('Restricted assignment with 2 processing times')
        model.hideOutput()

        # Decision variables
        x = {}
        for i in range(self.n_machines):
            for j in range(self.n_jobs):
                if self.processing_times[i][j] == '0':
                    x[i, j] = model.addVar(vtype="B", name=f"x({i},{j})", lb=0.0, ub=0.0)
                    #x[i, j] = 0
                else:
                    x[i, j] = model.addVar(vtype="B", name=f"x({i},{j})", lb=0.0)

        # Makespan
        C_max = model.addVar(vtype="C", name="C_max", lb=0.0)

        # Objective function
        model.setObjective(C_max, "minimize")

        # Constraint 1. You have to allocate each job
        for j in range(self.n_jobs):
            model.addCons(sum(x[i, j] for i in range(self.n_machines)) == 1)

        # Constraint 2. The processing time on each machine must be at most C_max
        for i in range(self.n_machines):
            model.addCons(sum(x[i, j] * int(self.processing_times[i][j]) for j in range(self.n_jobs)) <= C_max)

        # Print the model
        # model.writeProblem('model.lp')

        # Optimize the model
        model.optimize()
        # model.freeTransform()

        solution = list({j: i for j in range(self.n_jobs) for i in range(self.n_machines) if model.getVal(x[i, j]) > 0.5}.values())

        return solution, model.getObjVal()

    def gap(self):
        return self.opt_IP()[1] / self.opt_LP()
