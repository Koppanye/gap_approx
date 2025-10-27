from pyscipopt import Model
from itertools import combinations
import numpy as np

# TODO add possibility to hardcode instances
# TODO add possibility to manage the case where q = 0
class InstanceRestrictedAssignment():
    """
    Class for instances of the restricted assignment problem with integer processing times

    Parameters
    ----------
    See __init__()

    Attributes
    ----------
    See __init__()

    Methods
    -------
    opt_IP():
        Solve the integer programming formulation of the problem

    opt_configuration_LP():
        Solve the configuration LP of the problem
    """

    def __init__(self, n, m, generate, M = None, q = 0.1, distribution="uniform", p_max = 100, seed=1):
        """
        Constructor for the InstanceRestrictedAssignment class.
        Parameters
        ----------
        n : int
            Number of jobs
        m : int
            Number of machines
        q : float
            Probability of having a restriction (i.e., processing time of -1) in a machine-job pair
        p_max : int
            Maximum processing time for a job on a machine
        seed : int
            Random seed for reproducibility
        """
        self.n_jobs = n
        self.n_machines = m
        self.probability_of_restriction = q
        self.q = q
        self.p_max = p_max
        self.M = np.zeros((self.n_machines, self.n_jobs), dtype=int) # Machines x Jobs as in Jansen, Rohwedder 2017
        self.distribution = distribution

        if generate:
            # Basic checks
            assert 0 <= q <= 1, "Probability q must be between 0 and 1"

            # Set random seed for reproducibility
            np.random.seed(seed)

            for j in range(self.n_jobs):
                # Random processing time between 1 and p_max
                if self.distribution == "uniform":
                    p_j = np.random.randint(1, self.p_max)  # Random processing time between 1 and 100
                elif self.distribution == "exponential":
                    p_j = int(np.random.exponential(scale=self.p_max/5)) + 1
                    assert p_j > 0, "Processing time must be positive"
                    p_j = min(p_j, self.p_max)
                rng = np.random.default_rng()
                assignments = rng.binomial(1, self.q, self.n_machines)
                # If the max is 0, then trial again
                while len(set(assignments)) == 1:
                    assignments = rng.binomial(1, self.q, self.n_machines)
                self.M[:, j] = [p_j if assignments[i] == 0 else -1 for i in range(self.n_machines)]
        else:
            assert M is not None, "If generate is False, M must be provided"
            self.M = M


    def opt_LP(self, verbose=False, C_max = None):
        """
        Do a binary search to find the smallest integer for which is_feasible(T) is true.
        The initial guesses are as follows:
            l = highest processing time for any job - 1
            r = sum of all processing times
        We maintain the invariant that LB is in (l, r].

        Hint: as sometime we compute the integer value, just to speed up the computation, we provide the C_max as "right" initial guess.
        """
        right = sum(sum(int(self.M[i][j]) for j in range(self.n_jobs)) for i in range(self.n_machines))
        left = max(max(int(self.M[i][j]) for j in range(self.n_jobs)) for i in range(self.n_machines))-1
        if C_max != None:
            right = int(C_max)
        while right - left > 1:
            m = (left + right)//2
            is_feasible = self.is_feasible(m)
            if is_feasible:
                right = m
                if verbose:
                    print(f"LP feasible for T={m}")
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
        configs = {i: [c for length in range(1, self.n_jobs + 1) for c in combinations([j for j in range(self.n_jobs) if self.M[i][j] != -1], length) if sum(int(self.M[i][j]) for j in c) <= T] for i in range(self.n_machines)}

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

    def opt_IP(self, verbose=False):
        model = Model('Restricted assignment with 2 processing times')
        if not verbose:
            model.hideOutput()

        # Decision variables
        x = {}
        for i in range(self.n_machines):
            for j in range(self.n_jobs):
                if self.M[i][j] == 0:
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
            model.addCons(sum(x[i, j] * int(self.M[i][j]) for j in range(self.n_jobs)) <= C_max)

        # Print the model
        # model.writeProblem('model.lp')

        # Optimize the model
        model.optimize()
        # model.freeTransform()

        solution = list({j: i for j in range(self.n_jobs) for i in range(self.n_machines) if model.getVal(x[i, j]) > 0.5}.values())

        return solution, model.getObjVal()

    def gap(self):
        return self.opt_IP()[1] / self.opt_LP()
