#include <iostream>

#include <cmath>
#include <ctime>

#define N 16
using namespace std;


void configureRandomly(int board[][N], int *state) {
    // Seed for the random function
    srand(time(nullptr));
    for (int i = 0; i < N; i++) {
        // Getting a random row index
        state[i] = rand() % N;
        // Placing a queen on the
        board[state[i]][i] = 1;
    }
}
void printBoard(int board[][N])
{

    for (int i = 0; i < N; i++) {
        cout << " ";
        for (int j = 0; j < N; j++) {
            cout << board[i][j] << " ";
        }
        cout << "\n";
    }
}

bool compareStates(int *state1, int *state2) {

    for (int i = 0; i < N; i++) {
        if (state1[i] != state2[i]) {
            return false;
        }
    }
    return true;
}


void fill(int board[][N], int value) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            board[i][j] = value;
        }
    }
}


int calculateObjective(int board[][N], int *state) {

    int attacking = 0;
    int row, col;

    for (int i = 0; i < N; i++) {

        row = state[i], col = i - 1;
        while (col >= 0 && board[row][col] != 1) {
            col--;
        }
        if (col >= 0 && board[row][col] == 1) {
            attacking++;
        }

        row = state[i], col = i + 1;
        while (col < N && board[row][col] != 1) {
            col++;
        }
        if (col < N && board[row][col] == 1) {
            attacking++;
        }

        row = state[i] - 1, col = i - 1;
        while (col >= 0 && row >= 0 && board[row][col] != 1) {
            col--;
            row--;
        }
        if (col >= 0 && row >= 0 && board[row][col] == 1) {
            attacking++;
        }

        row = state[i] + 1, col = i + 1;
        while (col < N && row < N && board[row][col] != 1) {
            col++;
            row++;
        }
        if (col < N && row < N && board[row][col] == 1) {
            attacking++;
        }
        row = state[i] + 1, col = i - 1;
        while (col >= 0 && row < N && board[row][col] != 1) {
            col--;
            row++;
        }
        if (col >= 0 && row < N && board[row][col] == 1) {
            attacking++;
        }
        row = state[i] - 1, col = i + 1;
        while (col < N && row >= 0 && board[row][col] != 1) {
            col++;
            row--;
        }
        if (col < N && row >= 0 && board[row][col] == 1) {
            attacking++;
        }
    }

    // Return pairs.
    return (int) (attacking / 2);
}

void generateBoard(int board[][N],
                   int *state) {

    fill(board, 0);
    for (int i = 0; i < N; i++) {
        board[state[i]][i] = 1;
    }
}

void copyState(int *state1, int *state2) {

    for (int i = 0; i < N; i++) {
        state1[i] = state2[i];
    }
}

void getNeighbour(int board[][N], int *state) {

    int opBoard[N][N];
    int opState[N];
    copyState(opState, state);
    generateBoard(opBoard, opState);

    int opObjective = calculateObjective(opBoard, opState);

    int NeighbourBoard[N][N];
    int NeighbourState[N];

    copyState(NeighbourState, state);
    generateBoard(NeighbourBoard, NeighbourState);


    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {

            if (j != state[i]) {
                NeighbourState[i] = j;
                NeighbourBoard[NeighbourState[i]][i] = 1;

                NeighbourBoard[state[i]][i] = 0;
                int temp = calculateObjective(NeighbourBoard, NeighbourState);
                if (temp <= opObjective) {
                    opObjective = temp;
                    copyState(opState, NeighbourState);
                    generateBoard(opBoard, opState);
                }
                NeighbourBoard[NeighbourState[i]][i] = 0;
                NeighbourState[i] = state[i];
                NeighbourBoard[state[i]][i] = 1;
            }
        }
    }
    copyState(state, opState);
    fill(board, 0);
    generateBoard(board, state);
}

int hillClimbing(int board[][N], int *state) {

    int neighbourBoard[N][N] = {};
    int neighbourState[N];
    copyState(neighbourState, state);
    generateBoard(neighbourBoard, neighbourState);
    int iter = 0;
    do {
        iter++;
        copyState(state, neighbourState);
        generateBoard(board, state);
        getNeighbour(neighbourBoard, neighbourState);

        if (compareStates(state, neighbourState)) {
            printBoard(board);
            break;
        } else if (calculateObjective(board, state) == calculateObjective(neighbourBoard, neighbourState)) {
            neighbourState[rand() % N] = rand() % N;
            generateBoard(neighbourBoard, neighbourState);
        }
    } while (true);
    return iter;
}

// Driver code
#include <chrono>

using namespace std::chrono;



// the main function solve the nqueen problem and print the solution
// you can edit the N size in the global for any size you wish
// the function run k iteration for calculate average iteration ant timing
int main() {
    if (N == 2 || N == 3) {
        std::cout << "there is nosolution for n=2 or n=3 " << endl;
        return 0;
    }
    int sum = 0;
    long sum2 = 0;
    double k = 3;
    time_t time_1;
    time_t time_2;
    for (int i = 0; i < k; i++) {
        auto start = high_resolution_clock::now();
        int state[N] = {};
        int board[N][N] = {};
        // Getting a starting point by
        // randomly configuring the board
        configureRandomly(board, state);
        // Do hill climbing on the
        // board obtained
        int iter = hillClimbing(board, state);
        sum2 += iter;

        auto end = high_resolution_clock::now();
        auto duration = duration_cast<seconds>(end - start);
        sum += duration.count();
//        cout << "timing:" << duration.count();
//        cout << " iterations: "  << iter << endl;

    }

    sum2 /= k;
    std::cout << "avg iterations is :" << sum2 << endl;
    return 0;
}
