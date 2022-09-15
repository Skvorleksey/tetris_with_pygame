import shapes
import random


class Shape:
    def __init__(self):
        self.shapes = shapes.shapes
        self.current_shape = random.choice(shapes.shapes)
        self.next_shape = random.choice(shapes.shapes)
        self.x = 3
        self.y = 0

    def rotate_shape(self):
        width = len(self.current_shape)
        height = len(self.current_shape[0])
        new_shape = [[' '] * width for _ in range(height)]
        for i in range(width):
            for a in range(height):
                new_shape[a][width - 1 - i] = self.current_shape[i][a]
        self.current_shape = new_shape

    def get_new_shape(self):
        self.y = 0
        self.x = 3
        self.current_shape = self.next_shape
        self.next_shape = random.choice(shapes.shapes)

    def can_move_right(self, stack):
        for row, line in enumerate(self.current_shape):
            stack_line = stack[row + self.y]
            for i in range(len(line) - 1, -1, -1):
                if line[i] != ' ' and i + self.x + 1 < len(stack_line):
                    if stack_line[i + self.x + 1] != ' ':
                        return False
                    break
        return True

    def can_move_left(self, stack):
        for row, line in enumerate(self.current_shape):
            stack_line = stack[row + self.y]
            for col, cell in enumerate(line):
                if cell != ' ':
                    if stack_line[col + self.x - 1] != ' ':
                        return False
                    break

        return True
