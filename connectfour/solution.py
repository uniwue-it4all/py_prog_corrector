from enum import Enum
from typing import List

std_num_of_rows = 6
std_num_of_cols = 7

file_names = ['winner_x', 'winner_o'] #, 'no_winner']


class FieldState(Enum):
    UNMARKED = '_'
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'


class Cell:
    def __init__(self, cell_state: FieldState = None):
        self.state: FieldState = FieldState.UNMARKED if cell_state is None else cell_state

    def __str__(self) -> str:
        return str(self.state.value)


class Field:
    def __init__(self, rows: List[List[Cell]]):
        self.rows = rows

    def __str__(self) -> str:
        return "\n".join(map(Field.__print_row__, self.rows))

    @staticmethod
    def from_string(field_string: str) -> 'Field':
        return Field(rows=[Field.__row_from_string__(row_str) for row_str in field_string.strip().split('\n')])

    @staticmethod
    def __row_from_string__(row_string: str) -> List[Cell]:
        return [Cell(FieldState(cell_str)) for cell_str in row_string.split(' ')]

    @staticmethod
    def __print_row__(row: List[Cell]):
        return " ".join(map(str, row))

    def winner(self) -> FieldState:

        # Rows -> left to right, bottom to top
        for row in self.rows[::-1]:
            last_cell_state: FieldState = FieldState.UNMARKED
            current_streak = 0

            for cell in row:
                if cell.state is last_cell_state and last_cell_state is not FieldState.UNMARKED:
                    current_streak += 1
                last_cell_state = cell.state

                if current_streak == 4:
                    return last_cell_state.value

        max_streak = 0

        # Columns -> bottom to top, left to right
        for column_index in range(std_num_of_cols):
            last_cell_state: FieldState = FieldState.UNMARKED
            current_streak = 0

            for row_index in range(std_num_of_rows):
                cell = self.rows[row_index][column_index]
                if cell.state is last_cell_state and last_cell_state is not FieldState.UNMARKED:
                    current_streak += 1
                last_cell_state = cell.state

                if current_streak > max_streak:
                    max_streak = current_streak

                if current_streak == 4:
                    return last_cell_state.value

        print(max_streak)

        return FieldState.UNMARKED


if __name__ == "__main__":
    for file_name in file_names:
        with open(file_name, 'r') as file:
            test_field = Field.from_string(file.read())

            print(test_field)

            print("Winner in file '{}': {}".format(file.name, test_field.winner()))
