import random
import os

# check if the results files already exist so we can remove them to add new results

if os.path.isfile("playground/files/all_results_steps.txt"):
    os.remove("playground/files/all_results_steps.txt")

if os.path.isfile("playground/files/optimal_result_steps.txt"):
    os.remove("playground/files/optimal_result_steps.txt")


# declare the needed variables
numberOfShifts = 0
numberOfTasks = 0
taskTime = []
links = {}

# intialize variables


def Init():

    global numberOfShifts
    global numberOfShifts
    global taskTime
    global links

    numberOfShifts = 6
    numberOfTasks = 26

    for i in range(27):
        taskTime.append(0)
        links[i] = []

    # Read tasks.txt files to assign a time to each task
    with open('playground/files/tasks.txt') as f:

        while True:
            x = f.readline()

            if not x:
                break

            a = int(x.split(',')[0])
            b = int(x.split(',')[1].replace('\n', ''))
            taskTime[a] = b

    # Read task_links to link each task
    with open('playground/files/task_links.txt') as f:

        while True:

            x = f.readline()

            if not x:
                break

            a = int(x.split(',')[0])
            b = int(x.split(',')[1].replace('\n', ''))
            links[a].append(b)

# create random solutions


def CreateRandomSolutions():

    sol = []
    sol.append(False)
    sol.append(True)

    for i in range(25):
        sol.append(False)

    for i in range(numberOfShifts-1):
        index = random.randint(2, 26)
        while sol[index] == True:
            index = random.randint(1, 26)
        sol[index] = True

    return sol

# Create first population with the random solutions using CreateRandomSolutions function


def CreateInitialPopulation(size):

    solutions = []

    for _ in range(size):
        solution = CreateRandomSolutions()
        solutions.append(solution)

    return solutions


shift = []
vis = {}

for i in range(27):
    vis[i] = False

# dfs functions for traversing the shifts using the solution list


def DepthFirstSearch(u, sol):

    shift.append(u)
    vis[u] = True

    for v in links[u]:
        if sol[v] == False and vis[v] == False:
            DepthFirstSearch(v, sol)


# Single point crossover between 2 solutions
def SinglePointCrossover(s1, s2):

    index = random.randint(1, 26)
    newSolution = []

    for i in range(27):

        if i < index:
            newSolution.append(s1[i])
        else:
            newSolution.append(s2[i])

    return newSolution

# Swap Mutaion between two bits in the solution


def swap_mutaion(sol):

    index1 = random.randint(1, 26)
    index2 = random.randint(1, 26)

    while (sol[index1] ^ sol[index2]) == False:
        index1 = random.randint(1, 26)
        index2 = random.randint(1, 26)

    sol[index1], sol[index2] = sol[index2], sol[index1]


# Calculate Fitness by obtaining the maximum between times in each shifts
def CalculateFitnees(sol):

    maximumTime = 0

    for i in range(1, 27):

        if sol[i] == 1:

            DepthFirstSearch(i, sol)
            sumshift = 0
            for i in shift:
                sumshift += taskTime[i]

            maximumTime = max(maximumTime, sumshift)

            shift.clear()

    for i in range(27):
        vis[i] = False

    return maximumTime

# Write the soulution in txt files


def WriteSolutiom(sol, file_name, text):

    total_differences = 0
    maximumTime = -1
    minimumTime = 100000000000
    totalTime = sum(taskTime)
    rate = totalTime/numberOfShifts

    with open(file_name, 'a') as f:

        f.write(text)
        f.write('\n')

        for i in range(1, 27):

            if sol[i] == 1:

                DepthFirstSearch(i, sol)

                shift_sum = 0
                for i in shift:
                    shift_sum += taskTime[i]

                # print(shift)

                f.write(str(shift))
                f.write('\n')
                f.write("total time = " + str(shift_sum))
                f.write('\n')
                f.write("dif = " + str(abs(shift_sum - rate)))
                f.write('\n')

                total_differences += abs(shift_sum - rate)

                maximumTime = max(maximumTime, shift_sum)
                minimumTime = min(minimumTime, shift_sum)

                shift.clear()

        for i in range(27):
            vis[i] = False

        f.write("total time = " + str(totalTime))
        f.write('\n')
        f.write("total time / steps = " + str(rate))
        f.write('\n')
        f.write("total differences = " + str(total_differences))
        f.write('\n')
        f.write("average differences = " +
                str(total_differences/numberOfShifts))
        f.write('\n')
        f.write("max time = " + str(maximumTime))
        f.write('\n')
        f.write("min time = " + str(minimumTime))
        f.write('\n')
        f.write(
            '----------------------------------------------------------------------------------------------\n')


# main function to get the best solution
def Main(pop_size,max_itr,top):

    Init()

    popultaionSize = pop_size
    maxIter = max_itr
    top = top

    popultaion = CreateInitialPopulation(popultaionSize)

    bestGlobalResults = []
    for i in range(maxIter):

        bestResults = []

        for sol in popultaion:

            bestResults.append((sol, CalculateFitnees(sol)))
            WriteSolutiom(sol, 'playground/files/all_results_steps.txt',
                          'solution from iteration {} '.format(i+1))

        bestResults.sort(key=lambda x: x[1])

        new_population = []

        for solution in range(top):
            new_population.append(bestResults[0][0])

        children = []

        for _ in range(popultaionSize - top):

            idx1 = random.randint(0, top-1)
            idx2 = random.randint(0, top-1)

            child = SinglePointCrossover(
                new_population[idx1], new_population[idx2])

            swap_mutaion(child)

            children.append(child)

        new_population += children

        popultaion = new_population

        bestGlobalResults.append("Best result from iteration {} : {} ".format(
            i+1, bestResults[0][1]))
        if i == maxIter-1:
            WriteSolutiom(
                bestResults[0][0], 'playground/files/optimal_result_steps.txt', "Optimal solution")

    return bestGlobalResults



