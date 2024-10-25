#!/usr/bin/env python3

import itertools


state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return "".join(chr(x) for x in list(itertools.chain(*matrix)))


def add_round_key(s, k):
    return [
        [s[i][j] ^ k[i][j] for j in range(len(s[i]))] for i in range(len(s))
    ]


if __name__ == '__main__':
    print(matrix2bytes(add_round_key(state, round_key)))
