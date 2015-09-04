#!/usr/bin/env python
# encoding: utf-8
"""
The minigame 2048 in python
"""
import random
import curses


def init():
    """
    initialize a 2048 matrix. return a matrix list
    """
    matrix = [0] * 16
    random_lst = random.sample(range(16), 2)  # generate 2 different number
    matrix[random_lst[0]] = matrix[random_lst[1]] = 2
    return matrix


def move(matrix, direction):
    """
    moving the matrix. return a matrix list
    """
    mergedList = []  # initial the merged index
    if direction == 'w':
        for i in range(16):
            j = i
            while j - 4 >= 0:
                if matrix[j-4] == 0:
                    matrix[j-4] = matrix[j]
                    matrix[j] = 0
                elif matrix[j-4] == matrix[j] and j - 4 not in mergedList and j not in mergedList:
                    matrix[j-4] *= 2
                    matrix[j] = 0
                    mergedList.append(j-4)
                    mergedList.append(j)  # prevent the number to be merged twice
                j -= 4
    elif direction == 's':
        for i in range(15, -1, -1):
            j = i
            while j + 4 < 16:
                if matrix[j+4] == 0:
                    matrix[j+4] = matrix[j]
                    matrix[j] = 0
                elif matrix[j+4] == matrix[j] and j + 4 not in mergedList and j not in mergedList:
                    matrix[j+4] *= 2
                    matrix[j] = 0
                    mergedList.append(j)
                    mergedList.append(j+4)
                j += 4
    elif direction == 'a':
        for i in range(16):
            j = i
            while j % 4 != 0:
                if matrix[j-1] == 0:
                    matrix[j-1] = matrix[j]
                    matrix[j] = 0
                elif matrix[j-1] == matrix[j] and j - 1 not in mergedList and j not in mergedList:
                    matrix[j-1] *= 2
                    matrix[j] = 0
                    mergedList.append(j-1)
                    mergedList.append(j)
                j -= 1
    else:
        for i in range(15, -1, -1):
            j = i
            while j % 4 != 3:
                if matrix[j+1] == 0:
                    matrix[j+1] = matrix[j]
                    matrix[j] = 0
                elif matrix[j+1] == matrix[j] and j + 1 not in mergedList and j not in mergedList:
                    matrix[j+1] *= 2
                    matrix[j] = 0
                    mergedList.append(j)
                    mergedList.append(j+1)
                j += 1
    return matrix


def insert(matrix):
    """insert one 2 or 4 into the matrix. return the matrix list
    """
    getZeroIndex = []
    for i in range(16):
        if matrix[i] == 0:
            getZeroIndex.append(i)
    randomZeroIndex = random.choice(getZeroIndex)
    matrix[randomZeroIndex] = 2
    return matrix


def output(matrix):
    """
    print the matrix. return the matrix list
    """
    screen_str = ''
    max_num_width = len(str(max(matrix)))
    demarcation = ('+' + '-'*(max_num_width+2)) * 4 + '+'  # generate demarcation line like '+---+---+---+'
    # print(demarcation)
    screen_str += demarcation + '\n'
    for i in range(len(matrix)):
        if matrix[i] == 0:
            printchar = ' '
        else:
            printchar = str(matrix[i])
        # print '|',
        # print '{0:>{width}}'.format(printchar, width=max_num_width),
        screen_str += '|' + ' {0:>{width}} '.format(printchar, width=max_num_width)
        if (i + 1) % 4 == 0:
            # print '|'
            # print demarcation
            screen_str += '|\n' + demarcation + '\n'
    # print
    return screen_str

def isOver(matrix):
    """
    is game over? return bool
    """
    if 0 in matrix:
        return False
    else:
        for i in range(16):
            if i % 4 != 3:
                if matrix[i] == matrix[i+1]:
                    return False
            if i < 12:
                if matrix[i] == matrix [i+4]:
                    return False
    return True


def getchar(prompt="Wait input: "):
    import termios, sys
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON          # lflags
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        sys.stderr.write(prompt)
        sys.stderr.flush()
        c = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return c


def play():
    matrix = init()
    vim_mode = False
    vim_map = {'h': 'a', 'j': 's', 'k': 'w', 'l': 'd'}
    matrix_stack = []  # just used by back function
    matrix_stack.append(list(matrix))
    _step = len(matrix_stack) - 1

    # new way to print
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.nodelay(1)


    while True:
        # get matrix print string
        screen_str = output(matrix)

        # game is over?
        if isOver(matrix):
            # print 'Cannot move anyway. Game Over...'
            getchar('Cannot move anyway. Game Over...')
            break
        elif max(matrix) == 2048:
            _input = raw_input('The max number is 2048,you win the goal! q for quit, others for continue. ')
            if _input == 'q':
                break

        prompt = "[NORMAL] w(up)/s(down)/a(left)/d(right)"
        if vim_mode:
            prompt = "[VIM MODE] h:left, j:down, k:up, l:right"
        # _input = getchar(prompt='Step {0:2d} {1} q(quit) b(back) v(vim_mode): '.format(_step, prompt))
        screen_str += 'Step {0:2d} {1} q(quit) b(back) v(vim_mode): \n'.format(_step, prompt)
        screen.addstr(0, 0, screen_str)
        screen.refresh()
        _input = getchar(prompt='')
        screen.clear()
        if vim_mode:
            _input = vim_map.get(_input, _input)
        # print 'get:', _input
        if _input in ['w', 's', 'a', 'd']:
            matrix = move(matrix, _input)
            if matrix == matrix_stack[-1]:
                # print 'Not changed. Try another direction.'
                screen.refresh()
                screen.addstr(10, 0, 'Not changed. Try another direction.')
                screen.refresh()
            else:
                insert(matrix)
                matrix_stack.append(list(matrix))
                _step += 1
            continue
        elif _input == 'b':
            if len(matrix_stack) == 1:
                # print 'Cannot back anymore...'
                screen.refresh()
                screen.addstr(10, 0, 'Cannot back anymore..')
                screen.refresh()
                continue
            matrix_stack.pop()
            matrix = list(matrix_stack[-1])
            _step -= 1
            continue
        elif _input == 'q':
            break
        elif _input == 'v':
            vim_mode = not vim_mode
        else:
            print 'Input error! Try again.'

    # quit
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    print 'Byebye!'

if __name__ == '__main__':
    play()
