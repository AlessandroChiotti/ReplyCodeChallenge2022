import random
from typing import List
from input.input import Input
import math

class Problem:
    neighbors = 10
    initial_stamina = None
    max_stamina = None
    max_turns = None
    num_demons = None
    demons: List[dict]

    @staticmethod
    def init(input: Input):
        Problem.initial_stamina = input.initial_stamina
        Problem.max_stamina = input.max_stamina
        Problem.max_turns = input.max_turns
        Problem.num_demons = input.num_demons
        Problem.demons = input.demons

    @staticmethod
    def generate_initial_state():
        # initial_state = list(range(Problem.num_demons))
        # random.shuffle(initial_state)
        # return initial_state
    
        solution = Problem.demons.copy()
        cost_map = {}
        def objective_function_demon(demon):
            return round(sum(demon["fragments"]) / demon["required_stamina"])
        for index, demon in enumerate(solution):
            cost_map[index] = objective_function_demon(demon)
        #print(cost_map)
        return list({k: v for k, v in sorted(cost_map.items(), key=lambda item: item[1], reverse=True)}.keys())

    # @staticmethod
    # def generate_neighbor(demons_order: list):
    #     neighbor = demons_order.copy()
    #     i = random.randrange(Problem.num_demons)
    #     j = random.randrange(Problem.num_demons)
    #     neighbor[i] = demons_order[j]
    #     neighbor[j] = demons_order[i]
    #     return neighbor
    
    @staticmethod
    def generate_neighbor(demons_order: list):
        border = math.ceil((Problem.num_demons)/10) + 1
        return random.sample(demons_order[:border], border) + demons_order[border:]

    @staticmethod
    def generate_neighbors(demons_order: list) -> list:
        neighbors = list()
        for _ in range(Problem.neighbors):
            neighbors.append(Problem.generate_neighbor(demons_order))
        return neighbors

    @staticmethod
    def compute_cost(demons_order: list):
        current_stamina = Problem.initial_stamina
        stamina_per_turn = [0]*Problem.max_turns
        total_fragments = 0
        turn = 0
        i = 0

        while turn < Problem.max_turns:
            demon_index = demons_order[i]
            current_stamina = (current_stamina + stamina_per_turn[turn]) % (Problem.max_stamina + 1)
            demon = Problem.demons[demon_index]
            if current_stamina > demon["required_stamina"]:
                current_stamina -= demon["required_stamina"]
                if(turn + demon["turns_to_recover"] < Problem.max_turns):
                    stamina_per_turn[turn + demon["turns_to_recover"]] += demon["recovered_stamina"]
                total_fragments += sum(demon["fragments"][:min((Problem.max_turns - turn), demon["total_fragments"])])
                i += 1
            turn += 1

        return total_fragments
        
