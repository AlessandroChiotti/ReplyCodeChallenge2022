# from numpy import exp
# import random
# from problem.problem import Problem
# from state.state import State
# import sys


# class GeneticAlgorithm:

#     number_of_iterations = 1000

#     def __init__(self, initial_state: State):
#         self.initial_state = initial_state

#     def run(self):
#         """Peforms genetic algorithm to find a solution"""
#         print('GENETIC ALGORITHM')

#         # generate initial population
#         # population = Generate_Initial_Population(problem_size, population_size)

#         solution = int(sys.maxsize)
#         next_generation = []
#         n = 0

#         while n < self.number_of_iterations:

#             # get cost function for each data in population
#             population = Problem.Cost_Function(
#                 population=population, distances=distances, flows=flows)

#             # sort population according to fitness score
#             population.sort(key=lambda x: x[1])

#             # get fittest data
#             fittest_data = list.copy(population[0])

#             # check for the fittest data and print it out
#             if fittest_data[1] < solution:
#                 result = list.copy(fittest_data)
#                 solution = fittest_data[1]
#                 print("\nSolution for iteration - " + str(n))
#                 print(result)

#             while len(next_generation) < len(population):

#                 # use selection fucntion to get 2 fit chromosomes
#                 data1 = Selection_Function(population)
#                 data2 = Selection_Function(population)

#                 # crossover the 2 chromosome
#                 crossed_over_data = Crossover_Function(data1, data2)

#                 # mutate both chromosomes
#                 offspring1 = Mutation_Function(crossed_over_data[0])
#                 offspring2 = Mutation_Function(crossed_over_data[1])

#                 # add offsprings to next generation
#                 next_generation.append(offspring1)
#                 next_generation.append(offspring2)

#             # repeat iteration with new generation
#             population = next_generation
#             next_generation = []
#             n += 1

#         # print final result
#         print("Final solution after " + str(n) + " iterations = ")
#         print(result)

#         return result
