#! /usr/bin/env python

import sys


def read_board(lines):
    board = []
    for line in lines:
        board.append([int(n) for n in line.split()])

    return board


def score(board, number):
    score = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 'x':
                score += board[i][j]

    return score * number


def check_number(board, number):
    found = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == number:
                board[i][j] = 'x'
                found = (i, j)
                break
        if found is not None:
            break

    if found is not None:
        if all(n == 'x' for n in board[found[0]]):
            return score(board, number)
        if all(n == 'x'
               for n in [board[i][found[1]] for i in range(len(board[0]))]):
            return score(board, number)

    return None


def main(args):
    with open(args[0], 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    numbers = [int(n) for n in lines[0].split(',')]
    boards = []
    for i in range(1, len(lines), 6):
        boards.append(read_board(lines[i + 1:i + 6]))

    for number in numbers:
        for board in boards:
            score = check_number(board, number)
            if score is not None:
                print(score)
                return

    print('failed')


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
