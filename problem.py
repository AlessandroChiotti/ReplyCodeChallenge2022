import random
from input.input import Input


class Problem:
    neighbors = 10
    initial_stamina = None
    max_stamina = None
    max_turns = None
    num_demons = None
    demons = list
    index_fragments = list

    @staticmethod
    def init(input: Input):
        Problem.initial_stamina = input.initial_stamina
        Problem.max_stamina = input.max_stamina
        Problem.max_turns = input.max_turns
        Problem.num_demons = input.num_demons
        Problem.demons = input.demons
        Problem.index_fragments = [0]*(Problem.num_demons)

    @staticmethod
    def generate_initial_state():
        initial_state = list(range(Problem.num_demons))
        random.shuffle(initial_state)
        return initial_state

    @staticmethod
    def generate_neighbor(demons_order: list):
        neighbor = list(demons_order)
        random.shuffle(neighbor)
        return neighbor

    @staticmethod
    def generate_neighbors(demons_order: list) -> list:
        neighbors = list()
        for _ in range(Problem.neighbors):
            neighbors.append(Problem.generate_neighbor(demons_order))
        return neighbors

    

    @staticmethod
    def compute_cost(demons_order: list):
        print('calculating cost')
        demons = Problem.demons
        currently_summing = []
        total_reward = 0
        print('calculating turns')
        turns = Problem.compute_turn_demon(
            demons, Problem.max_turns, Problem.max_stamina, Problem.initial_stamina, demons_order)
        print('calculating rewards')
        for turn in turns:
            if turn != 'x':
                print(f'Start summing demon {turn}')
                demon_config = demons[turn]
                currently_summing.append(demon_config)
            for demon_config_elem in currently_summing:
                if demon_config_elem['index_fragment'] < len(demon_config_elem['fragments']):
                    total_reward += demon_config_elem['fragments'][demon_config_elem['index_fragment']]
                    demon_config_elem['index_fragment'] += 1

        return total_reward

    @staticmethod
    def compute_turn_demon(demons, max_turn: int, max_stamina: int, initial_stamina: int, solution):
        print('Compute turns')
        max_turn = Problem.max_turns
        max_stamina = Problem.max_stamina
        initial_stamina = Problem.initial_stamina
        #solution = [1, 3, 2, 4, 0]
        stamina = initial_stamina
        #reward = 0
        solution_pointer = 0
        turns = []
        recovered_stamina = [0] * (max_turn + 10)
        for i in range(max_turn):
            demon_number = solution[solution_pointer]
            print("Turn: " + str(i) + " stamina: " + str(stamina) +
                  " current pointer: " + str(solution_pointer))
            print("Recovering stamina: " + str(recovered_stamina[i]))
            stamina = stamina + recovered_stamina[i]
            demon_stamina = demons[demon_number]["consumed_stamina"]
            print("My stamina: " + str(stamina) +
                  " demon stamina: " + str(demon_stamina))
            if (stamina > demon_stamina):
                print("I have enough stamina to fight the demon")
                stamina = stamina - demon_stamina
                turns.append(demon_number)
                turn_in_witch_i_recover = (
                    i + demons[demon_number]["turns_to_recover"])
                print("In " + str(turn_in_witch_i_recover) + " i will recover " +
                      str(demons[demon_number]["recovered_stamina"]) + " stamina")
                recovered_stamina[turn_in_witch_i_recover] = demons[demon_number]["recovered_stamina"]
                solution_pointer = solution_pointer + 1
            else:
                turns.append("x")
        print(turns)
        return turns

    @staticmethod
    def compute_local_reward(num_turns_for_fragments: int, max_turns: int, current_turn: int, fragments):
        turn_earning = min(num_turns_for_fragments, max_turns - current_turn)
        reward = 0
        for i in range(0, turn_earning-1):
            reward = reward + fragments[i]
