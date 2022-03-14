import time

matrix = [[0 for i in range(101)] for i in range(101)]
row = [0 for i in range(101)]
forwardDiagonal = [0 for i in range(201)]
backwardDiagonal = [0 for i in range(201)]
iter = 0


def checkRow(row, n):
    for i in range(1, n + 1):
        if matrix[row][i] == 1:
            return True
    return False


def checkDiagonal(row, col, n):
    i = 1
    while row + i < n + 1 or row - i > 0 or col + i < n + 1 or col - i > 0:
        if row + i < n + 1 and col + i < n + 1 and matrix[row + i][col + i] == 1:
            return True
        if row + i < n + 1 and col - i > 0 and matrix[row + i][col - i] == 1:
            return True
        if row - i > 0 and col + i < n + 1 and matrix[row - i][col + i] == 1:
            return True
        if row - i > 0 and col - i > 0 and matrix[row - i][col - i] == 1:
            return True
        i += 1
    return False


def nqueens(n, col):
    for row in range(1, n + 1):
        if checkRow(row, n) == False and checkDiagonal(row, col, n) == False:
            matrix[row][col] = 1
            if col == n:
                return True
            flag = nqueens(n, col + 1)
            if flag == False:
                matrix[row][col] = 0
            else:
                return True
    return False


def Check(row1, col1, n):
    return row[row1] == True or forwardDiagonal[row1 + col1] == True or backwardDiagonal[
        2 * n - 1 + row1 - col1] == True


def Mark(row1, col1, n, arg):
    row[row1] = arg
    forwardDiagonal[row1 + col1] = arg
    backwardDiagonal[2 * n - 1 + row1 - col1] = arg


def nqueens_branc_bound(n, col):
    global iter
    for row in range(1, n + 1):
        iter += 1
        if not Check(row, col, n):
            matrix[row][col] = 1
            Mark(row, col, n, True)
            if col == n:
                return True
            flag = nqueens_branc_bound(n, col + 1)
            if not flag:
                matrix[row][col] = 0
                Mark(row, col, n, False)
            else:
                return True
    return False


def solve():
    global matrix, row, forwardDiagonal, backwardDiagonal, iter
    n = 32
    sum = 0
    sum_iter = 0
    for k in range(1):
        matrix = [[0 for i in range(101)] for i in range(101)]
        row = [0 for i in range(101)]
        forwardDiagonal = [0 for i in range(201)]
        backwardDiagonal = [0 for i in range(201)]
        iter = 0
        tic = time.perf_counter()
        sol = nqueens_branc_bound(n, 1)
        toc = time.perf_counter()
        if (not sol):
            print("Solution does not exist")
        sum += toc - tic
        sum_iter += iter
        print(f"{toc - tic:0.4f}")
    sum /= 1
    sum_iter /= 1
    print(f"solve the n-queen problem in branch and bound take in avg of 10 executions: {sum:0.4f} seconds with num iter {sum_iter}")


solve()
