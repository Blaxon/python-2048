#!/usr/bin/env python
# encoding: utf-8
"""
The mini game 2048 in python

this is the ai for 2048

require python3.x

What's new?
* scoring function add matrix transpose score
* update result presentation
* change monotonicity as penalty
* formalize 3 kind of weight

Author: Xander Hang
"""
import sys
import time


import game2048
import matrixmove


BOARD_DEFAULT_SCORE = 1000.0
EMPTY_WEIGHT = 200.0
MERGE_WEIGHT = 300.0
DIRECTION = {'w': ' up  ',
             's': 'down ',
             'a': 'left ',
             'd': 'right',
             '':  '     '}


def ai_play():
    matrix = game2048.init()
    step = 0
    move, score = '', 0

    while 1:
        # time.sleep(1)
        print_matrix(matrix)
        # is game over?
        if game2048.isOver(matrix):
            print("game over!")
            return max(matrix)
        if game2048.isWin(matrix):
            print("you win!")
            return 2048
        # find best move
        move, score = find_best_move(matrix)
        if move == 'n':
            break
        game2048.move(matrix, move)
        print('setp: %3d and the best move is %s with score %3d' % (step, DIRECTION[move], score))
        game2048.insert(matrix)
        step += 1
    print('ai finished.')


def print_matrix(matrix):
    i = 1
    for item in matrix:
        print('%5d' % item, end='')
        if i % 4 == 0:
            print('')
        i += 1


def find_best_move(matrix):
    best = 0
    best_move = None
    # for each direction calculate score
    for direction in ['w', 's', 'a', 'd']:
        _matrix, _score = game2048.move(matrix[:], direction)
        if _matrix == matrix:
            score = BOARD_DEFAULT_SCORE
        else:
            score = score_matrix(_matrix) + score_matrix(matrixmove.transpose(_matrix[:])) + \
                    _score * MERGE_WEIGHT
        if score > best:
            best = score
            best_move = direction
        print("The score of direction %s is %8d." % (DIRECTION[direction], score))
    return best_move, best


def score_matrix(matrix):
    score = BOARD_DEFAULT_SCORE
    for item in matrix:
        if item == 0:
            score += EMPTY_WEIGHT
    # monotonicity score
    score -= score_monotonicity(matrix)

    return score


def score_monotonicity(matrix):
    score_l = 0
    score_r = 0
    for i in [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]:
        sub = matrix[i-1] - matrix[i]
        if sub > 0:
            score_l += sub
        else:
            score_r -= sub
    return min(score_l, score_r)


def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Use the AI to play 2048 via browser control")
    parser.add_argument('-t', '--time', help="Times we test", type=int)

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    win_time = 0
    record = {2048: 0,
              1024: 0,
              512:  0,
              256:  0}

    start_time = time.time()
    for _ in range(1, args.time+1):
        score = ai_play()
        if score > 255:
            record[score] += 1
        if score == 2048:
            win_time += 1
    print('win %5d, fail %5d, probability: %3.3f, and total time takes %4.2f s' %\
          (win_time,
           args.time-win_time,
           float(win_time/args.time),
           time.time() - start_time))
    print('The score 2048 reaches %3d times' % record[2048])
    print('The score 1024 reaches %3d times' % record[1024])
    print('The score  512 reaches %3d times' % record[512])
    print('The score  256 reaches %3d times' % record[256])


if __name__ == '__main__':
    exit(main(sys.argv[1:]))

