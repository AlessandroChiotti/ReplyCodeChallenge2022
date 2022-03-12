# from state.state import State
# from simulated_annealing.simulated_annealing import SimulatedAnnealing
from input.input import Input
from output.output import Output
import random
from numpy import exp
import time

class State:
    cost = None
    demons_order: list

    def __init__(self, order: list):
        self.demons_order = order
    
    def get_cost(self):
        if self.cost is None:
            self.cost = Problem.compute_cost(self.demons_order)
        return self.cost
    
    def __str__(self):
        return f"State(demons_order={self.demons_order})"

class SimulatedAnnealing:
    initial_state: State
    initial_temp = 1000
    # final_temp = 0.1
    alpha = 0.85
    N = 40
    M = 300

    def __init__(self, initial_state: State):
        self.initial_state = initial_state

    def run(self):
        """Peforms simulated annealing to find a solution"""
        print('SIMULATED ANNEALING')
        
        current_temp = self.initial_temp

        # Start by initializing the current state with the initial state
        current_state = self.initial_state
        optimal_solution = current_state
        global_optimal_solution = current_state

        i = 0
        j = 0
        timeout = time.time() + 60*0.5   # 5 minutes from now

        for i in range(self.M):
            for j in range(self.N):
                #print('Generating solution')
                neighbor = State(random.choice(Problem.generate_neighbors(current_state.demons_order)))
                #print('Generated solution')
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
                    print('Found optimal solution')
                    global_optimal_solution = optimal_solution
                if time.time() > timeout:
                    break
            if time.time() > timeout:
                break

            current_state = optimal_solution

            # decrement the temperature
            current_temp = self.alpha * current_temp

        #print(f"Global optimal solution: {global_optimal_solution}")
        return global_optimal_solution

class Problem:
    neighbors = 10

    @staticmethod
    def init(input: Input):

        Problem.initial_stamina=input.initial_stamina
        Problem.max_stamina=input.max_stamina
        Problem.max_turns=input.max_turns
        Problem.num_demons=input.num_demons

        Problem.demons = [
            {
                "consumed_stamina": int(demon[0]),
                "turns_to_recover": int(demon[1]),
                "recovered_stamina": int(demon[2]),
                "total_fragments": int(demon[3]),
                "fragments": list(map(int, demon[4])),
                "index_fragment": 0
            } for demon in input.demons
        ]
    
    @staticmethod
    def generate_initial_state() -> list:
        return Problem.shuffled_immutable([i for i in range(Problem.num_demons)])

    def generate_initial_state_euristc():
        solution = Problem.demons.copy()
        cost_map = {}
        def objective_function_demon(demon):
            return round(sum(demon['fragments']) / demon['consumed_stamina'])
        for index, demon in enumerate(solution):
            cost_map[index] = objective_function_demon(demon)
        #print(cost_map)
        return list({k: v for k, v in sorted(cost_map.items(), key=lambda item: item[1], reverse=True)}.keys())
            

    @staticmethod
    def shuffled_immutable(gen):
        """

        """
        ls = list(gen)
        random.shuffle(ls)
        return ls
    
    @staticmethod
    def generate_neighbor(demons_order: list):
        border = len(demons_order)//10
        return Problem.shuffled_immutable(demons_order[:border]) + demons_order[border+1:]
    
    @staticmethod
    def generate_neighbors(demons_order: list) -> list:
        neighbors = list()
        for i in range(Problem.neighbors):
            neighbors.append(Problem.generate_neighbor(demons_order))
        return neighbors

    @staticmethod
    def compute_cost(demons_order: list):
        #print('calculating cost')
        demons = Problem.demons
        currently_summing = []
        total_reward = 0
        #print('calculating turns')
        turns = Problem.compute_turn_demon(demons, Problem.max_turns, Problem.max_stamina, Problem.initial_stamina, demons_order)
        #print('calculating rewards')
        for turn in turns:
            if turn != 'x':
                #print(f'Start summing demon {turn}')
                demon_config = demons[turn]
                currently_summing.append(demon_config)
                demon_config['index_fragment'] = 0
            for demon_config_elem in currently_summing:
                if demon_config_elem['index_fragment'] < len(demon_config_elem['fragments']):
                    total_reward += demon_config_elem['fragments'][demon_config_elem['index_fragment']]
                    demon_config_elem['index_fragment'] += 1

        return total_reward

    @staticmethod
    def compute_turn_demon(demons, max_turn: int, max_stamina: int, initial_stamina: int, solution):
        #print('Compute turns')
        max_turn = Problem.max_turns
        max_stamina = Problem.max_stamina
        initial_stamina = Problem.initial_stamina
        #solution = [1, 3, 2, 4, 0]
        stamina = initial_stamina
        #reward = 0
        solution_pointer = 0
        turns = []
        recovered_stamina = [0] * max_turn
        for i in range(max_turn):
            demon_number = solution[solution_pointer]
            #print("Turn: " + str(i) + " stamina: " + str(stamina) + " current pointer: " + str(solution_pointer))
            #print("Recovering stamina: " + str(recovered_stamina[i]))
            stamina = stamina + recovered_stamina[i]
            demon_stamina = demons[demon_number]["consumed_stamina"]
            #print("My stamina: " + str(stamina) + " demon stamina: " + str(demon_stamina))
            if (stamina > demon_stamina):
                #print("I have enough stamina to fight the demon")
                stamina = stamina - demon_stamina
                yield demon_number
                #turns.append(demon_number)
                turn_in_witch_i_recover = (i + demons[demon_number]["turns_to_recover"])
                if turn_in_witch_i_recover < max_turn:
                    #print ("In " + str(turn_in_witch_i_recover) + " i will recover " + str(demons[demon_number]["recovered_stamina"]) + " stamina")
                    recovered_stamina[turn_in_witch_i_recover] = demons[demon_number]["recovered_stamina"]
                solution_pointer = solution_pointer + 1
            else:
                #turns.append("x")
                yield 'x'
        #print(turns)
        #return turns

    @staticmethod
    def compute_local_reward(num_turns_for_fragments: int, max_turns: int, current_turn: int, fragments):
        turn_earning = min(num_turns_for_fragments, max_turns - current_turn)
        reward = 0
        for i in range(0, turn_earning-1):
            reward = reward + fragments[i]





def main():
    input = Input()
    input.read()
    # print(input)
    Problem.init(input)
    initial_state = Problem.generate_initial_state_euristc()
    #print(initial_state)
    solution = SimulatedAnnealing(State(initial_state)).run()
    print(f'Total reward: {Problem.compute_cost(solution.demons_order)}')
    output = Output(solution.demons_order, input.file_path)
    output.write()

if __name__ == "__main__":
    main()
