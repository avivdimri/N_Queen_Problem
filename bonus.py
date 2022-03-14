import numpy as np
import matplotlib.pyplot as plt


def isSafe(board, row, col, n):
    # Check this row on left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check lower diagonal on left side
    for i, j in zip(range(row, n, 1),
                    range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def solveNQUtil(board, col, n):
    if col >= n:
        return 1

    num_sols = 0
    for i in range(n):

        if isSafe(board, i, col, n):
            board[i][col] = 1
            num_sols += solveNQUtil(board, col + 1, n)
            board[i][col] = 0

    return num_sols


def solveNQ(n):
    board = np.zeros((n, n))
    res = solveNQUtil(board, 0, n)
    return res


def formula(n):
    return (0.143 * n) ** n


ref_compute_result = [1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200, 73712, 365596, 2279184, 14772512, 95815104,
                      666090624, 4968057848, 39029188884, 314666222712, 2691008701644, 24233937684440, 227514171973736,
                      2207893435808352, 22317699616364044, 234907967154122528]
n_list = range(1, len(ref_compute_result) + 1)
formula_result = [formula(n) for n in n_list]

# compute_result = []
# for n in tqdm(n_list):
#     compute_result.append(solveNQ(n))

plt.plot(n_list, formula_result, label='formula')
plt.plot(n_list, ref_compute_result, label='compute')
plt.title('Number of solutions for N queens problem')
plt.ylabel('Solution count (log scale)')
plt.xlabel('Board size')
plt.legend()
plt.grid()
plt.yscale('log')
plt.show()



