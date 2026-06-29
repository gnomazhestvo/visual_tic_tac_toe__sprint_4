import pygame
from gameparts.exceptions import FieldIndexError, CellOccupiedError

pygame.init()

# Константы игрового поля.
BOARD_SIZE = 3
CELL_SIZE = 100
SPACE = CELL_SIZE // 4
# Константы экрана.
BG_COLOR = (125, 125, 125)
SCREEN_HEIGHT = SCREEN_WIDTH = CELL_SIZE * BOARD_SIZE
FPS = 60
# Константы фигур.
LINE_WIDTH = 15
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)
X_WIDTH = 15
O_WIDTH = 15


class Board:
    """Класс логики игры Крестики-нолики."""

    def __init__(self):
        """Инициализация параметров."""
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in
                      range(BOARD_SIZE)]
        self.current_player = 'X'

    def make_move(self, row, cell, player):
        """Обработка хода игрока."""
        if self.board[row][cell] != ' ':
            raise CellOccupiedError
        self.board[row][cell] = player

    def make_turn(self, row, cell):
        """
        Выполняет ход.
        Возвращает True, если игра продолжается и False, если игра закончена.
        """
        try:
            self.make_move(row, cell, self.current_player)
        except CellOccupiedError:
            print('Выбранная ячейка занята.')
            return True
        except FieldIndexError:
            print('Неверные координаты.')
            return True
        # Проверяем, не закончена ли игра победой или ничьей.
        if self.check_win(self.current_player):
            result = f'Победили {self.current_player}'
            print(result)
            self.save_result(result)
            return False
        elif self.is_board_full():
            result = f'Ничья.'
            print(result)
            self.save_result(result)
            return False
        # Меняем игрока и, если игра продолжается, входим в цикл снова.
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_win(self, player):
        """Проверка победы."""
        # Проверка по горизонтали и по вертикали.
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player for j in range(BOARD_SIZE)):
                return True
            if all(self.board[j][i] == player for j in range(BOARD_SIZE)):
                return True

        # Проверка по диагоналям.
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)):
            return True
        if all(self.board[i][BOARD_SIZE - 1 - i] == player for i
                in range(BOARD_SIZE)):
            return True

        # Если ни вертикаль, ни горизонталь, ни диагональ, то False.
        return False

    def is_board_full(self):
        """Проверка заполненности поля."""
        for row in self.board:
            for cell in row:
                if cell == ' ':  # Нашли пустую ячейку
                    return False
        print('Все ячейки заполнены.')
        return True

    def save_result(self, result):
        with open('game_data.txt', 'a') as f:
            f.write(result + '\n')


class Game:
    """Отрисовка поляны для игры Крестики-нолики."""

    def __init__(self, board):
        """Инициализация атрибутов."""
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board = board

    def check_user_events(self):
        """Отслеживание действий игрока."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // CELL_SIZE
                cell = x // CELL_SIZE
                if not self.board.make_turn(row, cell):
                    self.running = False

    def draw_lines(self):
        """Отрисовка игрового поля."""
        for i in range(1, BOARD_SIZE):
            # Отрисовка горизонтальных линий.
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * CELL_SIZE),
                (SCREEN_WIDTH, i * CELL_SIZE),
                LINE_WIDTH
            )
            # Отрисовка вертикальных линий.
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (i * CELL_SIZE, 0),
                (i * CELL_SIZE, SCREEN_HEIGHT),
                LINE_WIDTH
            )

    def draw_figures(self):
        """Отрисовка элементов игры (крестики и нолики)."""
        for row in range(BOARD_SIZE):
            for cell in range(BOARD_SIZE):
                x = cell * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                offset = CELL_SIZE // 4

                if self.board.board[row][cell] == 'X':
                    pygame.draw.line(
                        self.screen,
                        X_COLOR,
                        (x - offset, y - offset),
                        (x + offset, y + offset),
                        X_WIDTH
                    )
                    pygame.draw.line(
                        self.screen,
                        X_COLOR,
                        (x + offset, y - offset),
                        (x - offset, y + offset),
                        X_WIDTH
                    )
                elif self.board.board[row][cell] == 'O':
                    pygame.draw.circle(
                        self.screen,
                        O_COLOR,
                        (x, y),
                        offset,
                        O_WIDTH
                    )

    def update_screen(self):
        """Обновление экрана."""
        self.screen.fill(BG_COLOR)
        self.draw_lines()
        self.draw_figures()
        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        """Запуск игры."""
        while self.running:
            self.check_user_events()
            self.update_screen()
        print('Игра закончена.')
        pygame.quit()


if __name__ == '__main__':
    board = Board()
    game = Game(board)
    game.main()