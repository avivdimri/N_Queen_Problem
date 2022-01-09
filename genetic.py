import time

counter = 0


class GeneticChess:

    def __init__(self, n):
        self.board = self.createBoard(n)
        self.solutions = []
        self.size = n
        self.env = []
        self.goal = None
        self.goalIndex = -1

    def createBoard(self, n):
        board = [[0 for i in range(n)] for j in range(n)]
        return board

    def setBoard(self, board, gen):
        for i in range(self.size):
            board[gen[i]][i] = 1

    def genereteDNA(self):
        # genereates random list of length n
        from random import shuffle
        DNA = list(range(self.size))
        shuffle(DNA)
        while DNA in self.env:
            shuffle(DNA)
        return DNA

    def initializeFirstGenereation(self):
        for i in range(100):
            self.env.append(self.genereteDNA())

    def utilityFunction(self, gen):

        hits = 0
        board = self.createBoard(self.size)
        self.setBoard(board, gen)
        col = 0

        for dna in gen:
            try:
                for i in range(col - 1, -1, -1):
                    if board[dna][i] == 1:
                        hits += 1
            except IndexError:
                print(gen)
                quit()
            for i, j in zip(range(dna - 1, -1, -1), range(col - 1, -1, -1)):
                if board[i][j] == 1:
                    hits += 1
            for i, j in zip(range(dna + 1, self.size, 1), range(col - 1, -1, -1)):
                if board[i][j] == 1:
                    hits += 1
            col += 1
        return hits

    def isGoalGen(self, gen):
        if self.utilityFunction(gen) == 0:
            return True
        return False

    def crossOverGens(self, firstGen, secondGen):

        isSwapped = False
        for i in range(1,len(firstGen)):
            if abs(firstGen[i-1] - firstGen[i])<2:
                isSwapped = True
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
            if abs(secondGen[i-1] - secondGen[i])<2:
                isSwapped = True
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
        if not isSwapped:
            bound = self.size//2
            for i in range(bound):
                 firstGen[i],secondGen[i] = secondGen[i],firstGen[i]

    # for i in range(1, len(firstGen)):
        #     if abs(firstGen[i - 1] - firstGen[i]) < 2:
        #         firstGen[i], secondGen[i] = secondGen[i], firstGen[i]
        #     if abs(secondGen[i - 1] - secondGen[i]) < 2:
        #         firstGen[i], secondGen[i] = secondGen[i], firstGen[i]

    def MutantGen(self, gen):

        bound = self.size // 2
        from random import randint as rand
        leftSideIndex = rand(0, bound)
        RightSideIndex = rand(bound + 1, self.size - 1)
        newGen = []
        for dna in gen:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.size):
            if i not in newGen:
                newGen.append(i)

        gen = newGen
        gen[leftSideIndex], gen[RightSideIndex] = gen[RightSideIndex], gen[leftSideIndex]
        return gen

    def crossOverAndMutant(self,f):
        for i in range(1, len(self.env), 2):
            firstGen = self.env[i - 1][:]
            secondGen = self.env[i][:]
            if f:
                print(f"firstGen is {firstGen} second gen is {secondGen}")
            self.crossOverGens(firstGen, secondGen)
            firstGen = self.MutantGen(firstGen)
            secondGen = self.MutantGen(secondGen)
            if f:
                print(f"firstGen is {firstGen} second gen is {secondGen}")
            self.env.append(firstGen)
            self.env.append(secondGen)

    def makeSelection(self):
        # index problem
        genUtilities = []
        newEnv = []

        for gen in self.env:
            genUtilities.append(self.utilityFunction(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil = None
        while len(newEnv) < self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])

        return newEnv

    def solveGA(self):
        self.initializeFirstGenereation()
        for gen in self.env:
            if self.isGoalGen(gen):
                return gen, 0
        count = 0
        f = False
        while count < 100:
            if count >50:
                f = True
            self.crossOverAndMutant(f)
            self.env = self.makeSelection()
            count += 1
            if self.goalIndex >= 0:
                try:
                    # print(count)
                    return self.goal, count
                except IndexError:
                    print(self.goalIndex)
            else:
                continue
        return None, count


sum = 0
j = 0
n=8
for i in range(10):
    start = time.perf_counter()
    chess = GeneticChess(n)
    solution, iter = chess.solveGA()
    end = time.perf_counter()
    if solution:
        sum += end - start
        j += 1
        print(f"Runtime in second:, {end - start:0.4f} with {iter} iterations")
        # print(f"solution is {solution}")
    else:
        print(f"failed with {iter} iterations")

if j > 0:
    sum /= j
print(f"solve the n-queen problem in genetic take in avg of {j} executions: {sum:0.4f} seconds")

