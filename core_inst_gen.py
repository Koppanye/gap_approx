"""
Given n (number of jobs), m (number of machines) and an error epsilon,
we wish to enumerate all core instances (m x n matrices with entries of the form k x epsilon)
with the following conditions:

  - The instance encoded by the matrix should have an LP-opt value that is at most 1.
  - In a given matrix, there can be at most 2 different finite entries. The rest of the values are all
    infinite.
  - In each column, all finite values must be the same (<-> machines are identical, apart from infinite values)

We want to enumerate them cleverly (disposing of symmetric or otherwise redundant cases), as the
number of all such instances is exponential in (n x m) and therefore it's infeasible to handle them
for (n x m) greater than 20. For this, we apply the following (implementation) tricks:

  - TODO
  - TODO
  - TODO

For each instance, we calculate LP-opt and IP-opt. Our upper bound on the empirical gap is
sup{ IP-opt / LP-opt } + (epsilon x n)
"""
from instance import Instance
from helper_funcs import majorate_iterator
from itertools import combinations, combinations_with_replacement, product
import math
import heapq


class bound_gap:
    def __init__(self, n, m, epsilon, stored_instance=20):
        self.n = n
        self.m = m
        self.epsilon = epsilon
        self.largest_num = int(1/self.epsilon)+1  # The largest integer we have to consider

        self.stored_instance = stored_instance
        self.best_gap = 1  # We record the highest gap found
        # We also record the best-many instances with the highest integrality gap for later studies,
        # with a min-heap of (gap, instance) pairs
        self.best_instances = [(1, '1'*(n*m))]
        self.gap_bound = None  # Once finished, it will be self.best_gap + self.n * self.epsilon

    def core_instance_generator(self):
        """
        We generate all possible pairs for 2 processing times (s, b), and call instance_iterator
        to enumerate all of them. Since the gap is invariant to rescaling, we discard all pairs
        whose ratio has been seen before. Due to the lexicographic enumeration,
        it happens iff gcd(s, b) != 1.
        """
        # We treat this case separately, as we have just 1 processing time
        self.instance_iterator(1, 1)

        for (s, b) in combinations(range(1, self.largest_num + 1), 2):
            # We simplify the fraction s/b by finding gcd(s,d)
            if math.gcd(s, b) == 1:
                self.instance_iterator(s, b)
        return True

    def instance_iterator(self, s, b):
        """
        For a given pair (s, b) in {(1, 1), (1, 2), ... , (1/epsilon, 1/epsilon)},
        we generate all inputs up to isomorphism and other redundancies.
        Considerations:
            - If an instance only contains either s or b, then it has already been visited.
              However, we still have to discard all other instances majorating it.
            - If an instance has an LP-optimum larger than 1, then it couldn't have been rounded down
              from an instance with LP-optimum equal to 1.
        """
        visited = set()
        """
        The already visited instances, plus the redundant ones: equivalent up to permutations, 
        or majorate an already seen instance. Whenever we process a new instance, we add
        all its permuted versions, and the ones that majorate it. Before processing a new instance,
        we check whether it is in visited or not. If it is, we pass; if it is not, we process it.
        The instances are stored in an m*n-long string in order to be unhashable.
        """
        for M in combinations_with_replacement(product(['0', str(s), str(b)], repeat=self.n), self.m):
            M = list(map(list, M))
            # We have to check whether M is valid or not (s and b cannot appear in the same column)
            valid = True
            for j in range(self.n):
                col = set(M[i][j] for i in range(self.m))
                if str(s) in col and str(b) in col:
                    valid = False
                    break

            if not valid:
                pass

            str_form = ''.join([''.join(M[i]) for i in range(self.m)])
            # If M is not in visited, we process it
            if str_form not in visited:
                instance = Instance(M)
                # If LP_opt > 1, we don't consider it. But we still throw away all of its permutations.
                X_frac, opt_frac = instance.opt_LP()
                if opt_frac <= 1:
                    X_int, opt_int = instance.opt_IP()
                    gap = instance.gap()
                    if len(self.best_instances) < self.stored_instance:
                        heapq.heappush(self.best_instances, (gap, str_form))
                    else:
                        heapq.heappushpop(self.best_instances, (gap, str_form))
                    forbidden_coords = X_int
                    """
                    TODO
                    transform it into a dict
                    """
                else:
                    forbidden_coords = {}
                # We have to loop through all matrices that majorate M, and
                # all their variants with permuted rows / columns, and add them to visited.
                majorate_iterator(M, forbidden_coords, visited)

        self.best_gap = heapq.nlargest(1, self.best_instances)[0]
        self.gap_bound = self.best_gap + self.n * self.epsilon
        return True
