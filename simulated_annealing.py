import random
from math import exp
import time
from copy import deepcopy

N_QUEENS = 1024
TEMPERATURE = 10000


def threat_calculate(n):
    '''Combination formular. It is choosing two queens in n queens'''
    if n < 2:
        return 0
    if n == 2:
        return 1
    return (n - 1) * n / 2


def create_board(n):
    '''Create a chess boad with a queen on a row best position to start with is puuting them on diagonal'''
    chess_board = {}
    for i in range(n):
        chess_board[i] =  n-1-i
    return chess_board


def cost(chess_board):
    '''Calculate how many pairs of threaten queen'''
    threat = 0
    m_chessboard = {}
    a_chessboard = {}

    for column in chess_board:
        temp_m = column - chess_board[column]
        temp_a = column + chess_board[column]
        if temp_m not in m_chessboard:
            m_chessboard[temp_m] = 1
        else:
            m_chessboard[temp_m] += 1
        if temp_a not in a_chessboard:
            a_chessboard[temp_a] = 1
        else:
            a_chessboard[temp_a] += 1

    for i in m_chessboard:
        threat += threat_calculate(m_chessboard[i])
    del m_chessboard

    for i in a_chessboard:
        threat += threat_calculate(a_chessboard[i])
    del a_chessboard

    return threat


def simulated_annealing():
    answer = create_board(N_QUEENS)
    # To avoid recounting when can not find a better state
    cost_answer = cost(answer)

    t = TEMPERATURE
    sch = 0.99
    it = 0
    while t > 0 and it < 300000:
        it +=1
        t *= sch
        successor = deepcopy(answer)
        while True:
            index_1 = random.randrange(0, N_QUEENS - 1)
            index_2 = random.randrange(0, N_QUEENS - 1)
            if index_1 != index_2:
                break
        successor[index_1], successor[index_2] = successor[index_2], \
            successor[index_1]  # swap two chosen queens
        delta = cost(successor) - cost_answer
        if delta < 0 or random.uniform(0, 1) < exp(-delta / t):
            answer = deepcopy(successor)
            cost_answer = cost(answer)
        if cost_answer == 0:
            return True,it

    return False,it


def print_chess_board(board):
    for column, row in board.items():
        print("{} => {}".format(column, row))


sum = 0
sum_iter=0
j = 0
for i in range(10):
    start = time.perf_counter()
    soultion,iter = simulated_annealing()
    end =  time.perf_counter()
    if soultion:
        sum += end - start
        sum_iter += iter
        j +=1
        print(f"Runtime in second:, {end - start:0.4f} with {iter} iterations")
        #print_chess_board(answer)
    else:
        print(f"failed with {iter} iterations")

if j>0:
    sum /= j
    sum_iter /= j
print(f"solve the n-queen problem in simulated annealing take in avg of {j} executions: {sum:0.4f} seconds with {sum_iter} iterations")
#print_chess_board(answer)




