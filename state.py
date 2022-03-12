from problem import Problem

class State:
    cost = None
    demons_order: list

    def __init__(self, demons_order: list):
        self.demons_order = demons_order

    def get_cost(self):
        if self.cost is None:
            self.cost = Problem.compute_cost(self.demons_order)
        return self.cost
    
    def generate_neighbors(self):
        return Problem.generate_neighbors(self.demons_order)
    
    def get_output_string(self):
        return "\n".join(map(str, self.demons_order))

    def __str__(self):
        return f"State(demons={self.demons_order})"
