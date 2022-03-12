from state import State

class Output:

    def __init__(self, solution: State, file_path):
        self.solution = solution
        self.file_path = file_path

    def write(self):
        with open(self.file_path, 'w') as outfile:
            outfile.write(self.solution.get_output_string())
