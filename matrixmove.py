#!/usr/bin/env python
# encoding: utf-8
"""
The minigame 2048 in python

this is the move part of 2048

"""
import time
import itertools

MOVE_TABLE_RIGHT = {}
MOVE_TABLE_LEFT = {}


def init_move_table():
    elements = [0] + [2**i for i in range(1, 12)]
    combinations = itertools.product(elements, repeat=4)

    print('initializing move table...', end='')
    time.sleep(1)
    for comb in combinations:
        comb = list(comb)
        res_r = row_move_right(comb[:])
        MOVE_TABLE_RIGHT[str(comb)] = res_r
        res_l = row_move_right(comb[::-1])[::-1]
        MOVE_TABLE_LEFT[str(comb)] = res_l
    print('done.')


def row_move_right(comb):
    """
    move only 1 row to the right
    :param comb:
    :return:
    """
    p1, p2 = -2, -1
    while p1 >= -4:
        if comb[p1] != 0:
            if comb[p2] == 0:
                comb[p2], comb[p1] = comb[p1], 0
                p1 -= 1
            elif comb[p2] == comb[p1]:
                comb[p2] *= 2
                comb[p1] = 0
                p1 -= 1
                p2 -= 1
            elif p1 - p2 < -1:
                p2 -= 1
                comb[p2], comb[p1] = comb[p1], 0
                p1 -= 1
            else:
                p1 -= 1
                p2 -= 1
        else:
            p1 -= 1
    return comb


def transpose(matrix):
    return [matrix[0], matrix[4], matrix[8], matrix[12],
            matrix[1], matrix[5], matrix[9], matrix[13],
            matrix[2], matrix[6], matrix[10], matrix[14],
            matrix[3], matrix[7], matrix[11], matrix[15]]


def move_up(matrix):
    ret = []
    _matrix = transpose(matrix)
    ret += MOVE_TABLE_LEFT[str(_matrix[0:4])]
    ret += MOVE_TABLE_LEFT[str(_matrix[4:8])]
    ret += MOVE_TABLE_LEFT[str(_matrix[8:12])]
    ret += MOVE_TABLE_LEFT[str(_matrix[12:16])]
    return transpose(ret)


def move_down(matrix):
    ret = []
    _matrix = transpose(matrix)
    ret += MOVE_TABLE_RIGHT[str(_matrix[0:4])]
    ret += MOVE_TABLE_RIGHT[str(_matrix[4:8])]
    ret += MOVE_TABLE_RIGHT[str(_matrix[8:12])]
    ret += MOVE_TABLE_RIGHT[str(_matrix[12:16])]
    return transpose(ret)


def move_left(matrix):
    ret = []
    ret += MOVE_TABLE_LEFT[str(matrix[0:4])]
    ret += MOVE_TABLE_LEFT[str(matrix[4:8])]
    ret += MOVE_TABLE_LEFT[str(matrix[8:12])]
    ret += MOVE_TABLE_LEFT[str(matrix[12:16])]
    return ret


def move_right(matrix):
    ret = []
    ret += MOVE_TABLE_RIGHT[str(matrix[0:4])]
    ret += MOVE_TABLE_RIGHT[str(matrix[4:8])]
    ret += MOVE_TABLE_RIGHT[str(matrix[8:12])]
    ret += MOVE_TABLE_RIGHT[str(matrix[12:16])]
    return ret

MATRIX_MOVE = {'w': move_up,
               's': move_down,
               'a': move_left,
               'd': move_right}
