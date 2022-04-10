from state import State
from numpy import exp
import random


class SimulatedAnnealing:
    initial_state: State
    initial_temp = 1000
    # final_temp = 0.1
    alpha = 0.85
    N = 40
    M = 300

    def __init__(self, initial_state):
        self.initial_state = initial_state

    def run(self):
        """Peforms simulated annealing to find a solution"""
        print('SIMULATED ANNEALING')

        current_temp = self.initial_temp

        # Start by initializing the current state with the initial state
        current_state = self.initial_state
        optimal_solution = current_state
        global_optimal_solution = current_state

        for i in range(self.M):
            for j in range(self.N):
                neighbor = (State)(random.choice(
                    current_state.generate_neighbors()
                ))

                # if the new solution is better, accept it
                if neighbor.get_cost() > optimal_solution.get_cost():
                    optimal_solution = neighbor
                # if the new solution is not better, accept it with a probability of e^(-cost/temp)
                else:
                    cost_diff = neighbor.get_cost() - optimal_solution.get_cost()
                    if random.random() <= exp(-cost_diff / current_temp):
                        optimal_solution = neighbor
                # if the new solution is better than the global one, accept it
                if optimal_solution.get_cost() > global_optimal_solution.get_cost():
                    print(f"New optimal solution found")
                    global_optimal_solution = optimal_solution

            current_state = optimal_solution
            # decrement the temperature
            current_temp = self.alpha * current_temp

        return global_optimal_solution
