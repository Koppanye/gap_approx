from itertools import combinations, permutations, product
import copy
import numpy as np


def majorate_iterator(M, forb_coords, vis_inst):
    """

    :param M: a matrix of size m x n; a valid input
    :param forb_coords: a dict with elements column: row, where each pair encodes a coordinate that
    must not be changed
    :param vis_inst: a set of already visited instances. We add each majorating instance with all
    of their permutations
    :return: nothing, we just modify vis_inst
    """
    modify_coords = [[i, j] for i in range(len(M)) for j in range(len(M[0])) if i != forb_coords[j] and M[i][j] != '0']
    for length in range(len(modify_coords)+1):
        for subset in combinations(modify_coords, length):
            M_new = copy.deepcopy(M)
            for (i, j) in subset:
                M_new[i][j] = '0'
            matrix_perm(M_new, vis_inst)


def matrix_perm(M, vis_inst):
    for row_perm, col_perm in product(permutations(range(len(M))), permutations(range(len(M[0])))):
        vis_inst.add(' '.join(list(np.array(M)[row_perm, :][:, col_perm].reshape(1, -1)[0])))
