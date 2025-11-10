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
    else:
        raise ValueError(f"Instance '{instance_string}' not recognized, must be one of\n" + \
                         f"jansen_land_maark_2018,\n" + f"jansen_land_maark_2018_modified,\n" + \
                            f"jansen_land_maark_2018_expanded\n"
                       )

    n = len(M[0])
    m = len(M)
    return n, m, M
