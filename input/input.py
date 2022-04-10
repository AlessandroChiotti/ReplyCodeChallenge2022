from typing import List


class Input:
    file_path = None
    demons: List[dict]
    max_stamina = None
    initial_stamina = None
    num_demons = None

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path) as infile:
            line = infile.readline().strip()
            self.initial_stamina, self.max_stamina, self.max_turns, self.num_demons = map(
                int, line.split(' '))
            self.demons = []
            for _ in range(self.num_demons):
                required_stamina, turns_to_recover, recovered_stamina, turns_to_get_fragments, * \
                    fragments = infile.readline().strip().split(' ')
                self.demons.append(
                    {
                        "required_stamina": int(required_stamina),
                        "turns_to_recover": int(turns_to_recover),
                        "recovered_stamina": int(recovered_stamina),
                        "total_fragments": int(turns_to_get_fragments),
                        "fragments": list(map(int, fragments))
                    }
                )

    def __str__(self):
        return f"Input(Player(initial_stamina={self.initial_stamina}, max_stamina={self.max_stamina}, max_turns={self.max_turns}, num_demons={self.num_demons}), demons={self.demons})"
