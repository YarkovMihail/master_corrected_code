from random import randint
from typing import Tuple

import pygame as pg

Pointer = Tuple[int, int]
Color = Tuple[int, int, int]

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

INITIAL_SNAKE_POSITION: Tuple[int, int] = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2
)

UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)
BORDER_COLOR: Color = (93, 216, 228)
APPLE_COLOR: Color = (255, 0, 0)
SNAKE_COLOR: Color = (0, 255, 0)
SPEED: int = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position: Pointer = INITIAL_SNAKE_POSITION,
        body_color: Color = None
    ) -> None:
        """
        Инициализация игрового объекта.

        Args:
            position: позиция объекта на экране.
            body_color: цвет объекта в формате RGB.
        """
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Отрисовать объект на экране."""
        raise NotImplementedError('Метод должен быть реализован в наследнике')


class Apple(GameObject):
    """Класс яблока в игре «Змейка»."""

    def __init__(self, occupied_positions: list[tuple[int, int]] = None):
        # tuple[int, int], dict[str, list[tuple[int]]], int/float и т.д.
        """Инициализация яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions: list[tuple[int, int]]) -> None:
        # tuple[int, int], dict[str, list[tuple[int]]], int/float и т.д.
        """Разместить яблоко на поле, избегая занятых позиций."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self) -> None:
        """Отрисовать яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки в игре."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length: int = 1
        self.positions: list[Tuple[int, int]] = [INITIAL_SNAKE_POSITION]
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer | None = None
        self.last: Tuple[int, int] | None = None

    def update_direction(self) -> None:
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Переместить змейку на одну клетку."""
        head = self.get_head_position()
        head_x, head_y = head
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.last = self.positions[-1]
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self) -> Tuple[int, int]:
        """Получить позицию головы змейки.

        Returns:
            Координаты головы змейки.
        """
        return self.positions[0]

    def reset(self) -> None:
        """Сбросить змейку в начальное состояние."""
        self.length = 1
        self.positions = [INITIAL_SNAKE_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self) -> None:
        """Отрисовать змейку на экране."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake) -> None:
    """Обработать нажатия клавиш.

    Args:
        game_object: объект змейки для управления.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция игры — запуск игрового цикла."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if head in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
