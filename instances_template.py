import numpy as np

def pick_one_instance(instance_string):
    if instance_string == "jansen_land_maark_2018":
        M = [
            [1, 1, 1, 0, 0, 0, 0],
            [0, 1, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1]
        ]
    elif instance_string == "jansen_land_maark_2018_modified":
        M = [
            [1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1]
        ]
    elif instance_string == "jansen_land_maark_2018_expanded":
        # This has IG = 1
        M = [
            [1,     1,  1,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0,    1,  1,  1,  1,  1,  0, 0, 0, 0, 0, 0, 0],
            [0,    0, 0, 1,  1,  1,  0, 0, 0, 0, 0, 0, 0],
            [0,    0, 0, 1,  1,  1,  2,  0, 0, 0, 0, 0, 0],
            [0,    0, 0, 0, 0, 0, 2,  1,  1,  1,  0, 0, 0],
            [0,    0, 0, 0, 0, 0, 0, 1,  1,  1,  0, 0, 0],
            [0,    0, 0, 0, 0, 0, 0, 1,  1,  1,  1,  1,  0],
            [0,    0, 0, 0, 0, 0, 0, 0,0, 0,  1,  1,   1],
        ]
    elif instance_string == "koppany_2025":
        # Block 1
        M_1 = np.ones((3, 5))
        M_2 = np.ones((4, 3))
        M_3 = np.ones((2, 3))

        n_machines = 9
        n_jobs = 13

        M = np.zeros((n_machines, n_jobs))

        M[:3, :5] = M_1
        M[[2, 3], 5] = [2, 2]
        M[3:7, [6, 7, 8]] = M_2
        M[[6, 7], 9] = [2, 2]
        M[7:9, 10:13] = M_3

        M = M.tolist()
    elif instance_string == "koppany_2025_short":
        M = [
            [   1,  1,  1,  0,  0,  0,  0,  0,  0],
            [   1,  1,  1,  2,  0,  0,  0,  0,  0],
            [   0,  0,  0,  2,  1,  0,  0,  0,  0],
            [   0,  0,  0,  0,  1,  0,  0,  0,  0],
            [   0,  0,  0,  0,  1,  2,  0,  0,  0],
            [   0,  0,  0,  0,  0,  2,  1,  1,  1],
            [   0,  0,  0,  0,  0,  0,  1,  1,  1],
        ]

    else:
        raise ValueError(f"Instance '{instance_string}' not recognized, must be one of\n" + \
                         f"jansen_land_maark_2018,\n" + f"jansen_land_maark_2018_modified,\n" + \
                            f"jansen_land_maark_2018_expanded\n" + "koppany_2025\n" + \
                         "koppany_2025_short"
                       )

    n = len(M[0])
    m = len(M)
    return n, m, M
