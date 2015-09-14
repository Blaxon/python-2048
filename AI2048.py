#!/usr/bin/env python
# encoding: utf-8
"""
The minigame 2048 in python

this is the ai for 2048

"""
import os
import sys
import time


import game2048


DIRECTION = {'w': 'up',
             's': 'down',
             'a': 'left',
             'd': 'right',
             '': ''}


def ai_play():
    matrix = game2048.init()
    step = 0
    move, score = '', 0

    while 1:
        # time.sleep(1)
        print_matrix(matrix)
        print('setp: %3d and the best move is %s with score %4d' % (step, DIRECTION[move], score))
        # is game over?
        if game2048.isOver(matrix):
            print("game over!")
            return 'f'
        if game2048.isWin(matrix):
            print("you win!")
            return 'w'
        # find best move
        move, score = find_best_move(matrix)
        if move == 'n':
            break
        game2048.move(matrix, move)
        game2048.insert(matrix)
        step += 1
    print('ai finished.')


def print_matrix(matrix):
    i = 1
    for item in matrix:
        print('%5d' % item),
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
    return best_move, best


def score_matrix(matrix):
    score = 0
    for item in matrix:
        if item == 0:
            score += 1
    return score


def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Use the AI to play 2048 via browser control")
    parser.add_argument('-t', '--time', help="Times we test", type=int)

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    win_time = 0
    for _ in range(1, args.time+1):
        if ai_play() == 'w':
            win_time += 1
    print('win %5d, fail %5d, probability: %3.3f' % (win_time, args.time-win_time, float(win_time/args.time)))


if __name__ == '__main__':
    exit(main(sys.argv[1:]))

