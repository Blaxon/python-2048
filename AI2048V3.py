#!/usr/bin/env python
# encoding: utf-8
"""
The mini game 2048 in python

this is the ai for 2048

require python3.x

What's new?
* rollback and use V1's move function,its more efficient.
* add monotonicity function to calc score
* show max score we reach in terminal,and show its counter

"""
import os
import sys
import time


import game2048
import matrixmove


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
        _matrix = game2048.move(matrix[:], direction)
        if _matrix == matrix:
            score = 0
        else:
            score = score_matrix(_matrix)
        if score > best:
            best = score
            best_move = direction
        print("The score of direction %s is %8d." % (DIRECTION[direction], score))
    return best_move, best


def score_matrix(matrix):
    score = 0
    for item in matrix:
        if item == 0:
            score += 10
    # monotonicity score
    score += score_monotonicity(matrix)

    return score


def score_monotonicity(matrix):
    score_g = 0
    score_l = 0
    for i in [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]:
        if matrix[i-1] >= matrix[i]:
            score_g += 2
        else:
            score_l += 2
    return max(score_l, score_g)


def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Use the AI to play 2048 via browser control")
    parser.add_argument('-t', '--time', help="Times we test", type=int)

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    win_time = 0
    max_score = 0
    max_score_time = 0

    start_time = time.time()
    for _ in range(1, args.time+1):
        score = ai_play()
        if score == max_score:
            max_score_time += 1
        if score > max_score:
            max_score = score
            max_score_time = 1
        if score == 2048:
            win_time += 1
    print('win %5d, fail %5d, probability: %3.3f, the max score is %4d[%2d] , and total time takes %4.2f s' %\
          (win_time,
           args.time-win_time,
           float(win_time/args.time),
           max_score,
           max_score_time,
           time.time() - start_time))


if __name__ == '__main__':
    exit(main(sys.argv[1:]))

