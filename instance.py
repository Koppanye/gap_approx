class Instance:
    def __init__(self, M):
        self.processing_times = M
        self.n_jobs = len(M[0])
        self.n_machines = len(M)

    def opt_LP(self):
        return

    def is_feasible(self, T):
        return

    def opt_IP(self):
        return
