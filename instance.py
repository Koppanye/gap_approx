class Instance:
    def __init__(self, M):
        self.processing_times = M   # An m x n tuple of tuples with string values '0', 's', 'b'
        self.n_jobs = len(M[0])
        self.n_machines = len(M)

    def opt_LP(self):
        return X_frac, opt_frac

    def is_feasible(self, T):
        return True

    def opt_IP(self):
        return X_int, opt_int

    def gap(self):
        return self.opt_IP()[1] / self.opt_LP()[1]
