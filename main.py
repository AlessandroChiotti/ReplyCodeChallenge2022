from input.input import Input
from output.output import Output
from problem import Problem
from state import State
from simulated_annealing.simulated_annealing import SimulatedAnnealing

INPUT_FOLDER_PATH = "./input"
OUTPUT_FOLDER_PATH = "./output"
INPUT_FILE_NAME = [
    "00-example.txt",
    "01-the-cloud-abyss.txt",
    "02-iot-island-of-terror.txt",
    "03-etheryum.txt",
    "04-the-desert-of-autonomous-machines.txt",
    "05-androids-armageddon.txt"
]
input_file_name = INPUT_FILE_NAME[0]
output_file_name = f"output-{input_file_name}"
input_file_path = f"{INPUT_FOLDER_PATH}/{input_file_name}"
output_file_path = f"{OUTPUT_FOLDER_PATH}/{output_file_name}"

def main():
    input = Input(input_file_path)
    input.read()
    Problem.init(input)
    initial_state = State(Problem.generate_initial_state())
    solution = SimulatedAnnealing(initial_state).run()
    print(f'Total reward: {solution.get_cost()}')
    output = Output(solution, output_file_path)
    output.write()


if __name__ == "__main__":
    main()
