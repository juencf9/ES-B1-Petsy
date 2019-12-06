import numpy as np


def levenshtein_func(seq1, seq2):
    """
    Levenshtein function between two sequences.
    :param seq1: Sequence 1
    :param seq2: Sequence 2
    :return: Edit distance between seq1 and seq2
    """

    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            # Costs are used in a way that substitution and delete are costly, but addition is fairly cheap
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 3,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 3
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 2,
                    matrix[x-1,y-1] + 6,
                    matrix[x,y-1] + 6
                )

    return matrix[size_x - 1, size_y - 1]