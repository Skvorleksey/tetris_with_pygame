import pygame
import sys

from shape import Shape

pygame.font.init()

OUTER_COLOR = (8, 31, 105)
INNER_COLOR = (0, 0, 0)
CELL_COLOR = (220, 220, 220)

cell_colors = {
    '1': (241, 144, 102),
    '2': (245, 205, 121),
    '3': (84, 109, 229),
    '4': (225, 95, 65),
    '5': (196, 69, 105),
    '6': (248, 165, 194),
    '7': (87, 75, 144),
}

first_player_buttons = {
    'left': pygame.K_LEFT,
    'rotate': pygame.K_UP,
    'right': pygame.K_RIGHT,
    'down': pygame.K_DOWN,
}
second_player_buttons = {
    'left': pygame.K_a,
    'rotate': pygame.K_w,
    'right': pygame.K_d,
    'down': pygame.K_s,
}


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, color, text_color):
        super().__init__()
        self.font = pygame.font.Font(None, 30)
        self.text_image = self.font.render(text, True, text_color)
        self.rect, self.image = self.create_image_and_rect(x, y, width, height, color)

    def create_image_and_rect(self, x, y, width, height, color):
        image = pygame.surface.Surface((width, height))
        image.fill(color)
        image.blit(
            self.text_image,
            ((image.get_width() / 2 - self.text_image.get_width() / 2),
             (image.get_height() / 2 - self.text_image.get_height() / 2))
        )
        rect = image.get_rect(center=(x, y))
        return rect, image

    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 500))
        self.buttons = pygame.sprite.Group()

        self.single_game_button = Button(self.screen.get_width() / 2, 100, 200, 50, 'Single game',
                                         (255, 255, 255), (0, 0, 0))
        self.game_for_two_button = Button(self.screen.get_width() / 2, 200, 200, 50, 'Game for two',
                                          (255, 255, 255), (0, 0, 0))
        self.exit_button = Button(self.screen.get_width()/2, 300, 200, 50, 'Exit',
                                  (255, 255, 255), (0, 0, 0))
        self.buttons.add((self.single_game_button, self.game_for_two_button, self.exit_button))
        self.main()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update_screen(self):
        self.screen.fill((125, 125, 200))
        self.buttons.draw(self.screen)
        pygame.display.flip()

    def single_game(self):
        tetris = Tetris(50, 0, first_player_buttons)
        group = pygame.sprite.Group((tetris,))

        while not tetris.is_game_over():
            for event in pygame.event.get():
                if tetris.control(event):
                    break
            tetris.logic()
            tetris.draw()
            group.draw(self.screen)
            pygame.display.flip()
            tetris.clock.tick(3)

    def game_for_two(self):
        tetris1 = Tetris(0, 0, second_player_buttons)
        tetris2 = Tetris(500, 0, first_player_buttons)
        group = pygame.sprite.Group((tetris1, tetris2))
        run = True

        while not tetris1.is_game_over() and not tetris2.is_game_over() and run:
            for event in pygame.event.get():
                tetris1.control(event)
                tetris2.control(event)
            if tetris1.logic():
                run = False
                break
            if tetris2.logic():
                run = False
                break
            tetris1.draw()
            tetris2.draw()

            group.draw(self.screen)
            pygame.display.flip()
            tetris1.clock.tick(3)

    def main(self):
        while True:
            self.check_events()
            self.update_screen()
            if self.single_game_button.is_clicked():
                self.single_game()
            elif self.game_for_two_button.is_clicked():
                self.game_for_two()
            elif self.exit_button.is_clicked():
                sys.exit()


class Tetris(pygame.sprite.Sprite):
    def __init__(self, x, y, buttons):
        super().__init__()
        self.ground_width = 10
        self.ground_height = 20
        self.cell_size = 20
        self.buttons = buttons

        self.image = pygame.surface.Surface((500, 500))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clock = pygame.time.Clock()

        self.game_display = pygame.Surface((self.ground_width * self.cell_size, self.ground_height * self.cell_size))

        self.is_game_on = True
        self.greeting()
        self.ground = [[' '] * self.ground_width for _ in range(self.ground_height)]
        self.lines = 0
        self.scores = 0
        self.level = 1

        self.font = pygame.font.Font(None, 30)
        self.lines_text = self.font.render(f'Lines: {self.lines}', True, CELL_COLOR)
        self.scores_text = self.font.render(f'Scores: {self.lines}', True, CELL_COLOR)
        self.next_text = self.font.render('Next:', True, CELL_COLOR)
        self.side_panel_x = 220

        self.shape = Shape()

        self.stack = [[' '] * self.ground_width for _ in range(self.ground_height)]

        self.draw()

    @staticmethod
    def greeting():
        print("Welcome to tetris game!\n")

    def show_next(self, x, y):
        for row, line in enumerate(self.shape.next_shape):
            for col, cell in enumerate(line):
                if cell != ' ':
                    pygame.draw.rect(
                        self.image,
                        cell_colors[cell],
                        (col * self.cell_size + x, row * self.cell_size + y + 30, self.cell_size, self.cell_size))

        self.image.blit(self.next_text, (x, y))

    def draw(self):
        # refresh background
        self.image.fill(OUTER_COLOR)
        self.game_display.fill(INNER_COLOR)

        self.show_next(self.side_panel_x, 20)

        self.image.blit(self.lines_text, (self.side_panel_x, 150))
        self.image.blit(self.scores_text, (self.side_panel_x, 200))

        # refresh map
        self.ground = [[' '] * self.ground_width for _ in range(self.ground_height)]

        # add stack cells to map
        for y, line in enumerate(self.stack):
            for x, cell in enumerate(line):
                if cell != ' ':
                    self.ground[y][x] = cell

        # add current shape cells to map
        for y, line in enumerate(self.shape.current_shape):
            for x, cell in enumerate(line):
                if cell != ' ':
                    self.ground[self.shape.y + y][self.shape.x + x] = cell

        # draw cells on inner display
        for row, line in enumerate(self.ground):
            for col, cell in enumerate(line):
                if cell != ' ':
                    pygame.draw.rect(
                        self.game_display,
                        cell_colors[cell],
                        (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),
                    )

        # draw inner display on main window
        self.image.blit(self.game_display, (10, 10))

    def logic(self):
        # gravity
        self.shape.y += 1

        # check side edges collision
        if self.shape.x < 0:
            self.shape.x = 0
        elif self.shape.x + len(self.shape.current_shape[0]) > self.ground_width:
            self.shape.x = self.ground_width - len(self.shape.current_shape[0])

        # check stack collisions
        if self.is_touch_stack():
            for y, line in enumerate(self.shape.current_shape):
                for x, cell in enumerate(line):
                    if cell != ' ':
                        self.stack[self.shape.y + y][self.shape.x + x] = cell

            self.shape.get_new_shape()

        # check bottom collision
        elif self.shape.y + len(self.shape.current_shape) >= self.ground_height + 1:
            for y, line in enumerate(self.shape.current_shape):
                for x, cell in enumerate(line):
                    if cell != ' ':
                        self.stack[self.shape.y + y - 1][self.shape.x + x] = cell

            self.shape.get_new_shape()

        # check completed lines
        multiply_rate = {1: 1, 2: 3, 3: 5, 4: 8}
        completed = 0
        for line in self.stack:
            if ' ' not in line:
                self.stack.remove(line)
                self.stack.insert(0, [' '] * self.ground_width)
                completed += 1

        if completed:
            self.lines += completed
            self.scores += 100 * self.level * multiply_rate[completed]
            self.lines_text = self.font.render(f'Lines: {self.lines}', True, CELL_COLOR)
            self.scores_text = self.font.render(f'Scores: {self.scores}', True, CELL_COLOR)

    def is_game_over(self):
        for col in range(3, 7):
            if (row := self.get_highest_stack_point(col)) <= 2 and (row != -1):
                return True

    def is_touch_stack(self):
        col_range = [i + self.shape.x for i in range(len(self.shape.current_shape[0]))]
        for col in col_range:
            if self.get_highest_stack_point(col) - self.get_lowest_shape_point(col) == 1:
                return True

    def get_highest_stack_point(self, col):
        for row, line in enumerate(self.stack[self.shape.y:], self.shape.y):
            if line[col] != ' ':
                return row
        return -1

    def get_lowest_shape_point(self, col):
        for i in range(len(self.shape.current_shape) - 1, -1, -1):
            if self.shape.current_shape[i][col-self.shape.x] != ' ':
                return i + self.shape.y

    def control(self, event):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        #     elif event.type == pygame.KEYDOWN:
        if event.type == pygame.KEYDOWN:
            if event.key == self.buttons['left'] and self.shape.can_move_left(self.stack):
                self.shape.x -= 1
            if event.key == self.buttons['right'] and self.shape.can_move_right(self.stack):
                self.shape.x += 1
            if event.key == self.buttons['rotate']:
                self.shape.rotate_shape()
            if event.key == self.buttons['down']:
                self.scores += 1
            if event.key == pygame.K_x:
                print('Bye!')
                self.is_game_on = False
                return True

    def run(self):
        while self.is_game_on:
            if self.control():
                break
            self.logic()
            if self.is_game_over():
                print('Game over!')
                self.is_game_on = False

            pygame.display.flip()

            self.draw()

            pygame.display.flip()

            self.clock.tick(3)


# Tetris()
Game()
