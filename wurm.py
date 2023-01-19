import tkinter as tk
from tkinter import ttk
import random
from enum import Enum
import logging


# TODO:
# 1. no walking back through self
# 2. collision detection and gameover
# 3. factor out App from GameBoard
# 4. fix hardcoded board dimensions
# 5. Add scoring, hud
# 6. add additional configuration options (e.g. tick speed, starting length, toggle walls) and CLI


class Direction(Enum):
    UP = "w"
    DOWN = "s"
    LEFT = "a"
    RIGHT = "d"


class Snake:
    def __init__(self, head_color: str = "red", body_color: str = "green"):
        self._stack = [(20, 20), (20, 21), (20, 22), (20, 23)]
        self.length = len(self._stack)  # this should be a property
        self._direction = Direction.UP
        self.head_color = head_color
        self.body_color = body_color

    @property
    def head(self):
        return self._stack[0]

    def move(self):
        head = self._stack.pop(0)
        tmp = head
        self._stack.insert(0, tmp)
        # hardcoded board dimensions
        match self.direction:
            case Direction.DOWN:
                head = (head[0], (head[1] + 1) % (1000 // 10))
            case Direction.UP:
                head = (head[0], (head[1] - 1) % (1000 // 10))
            case Direction.LEFT:
                head = ((head[0] - 1) % (1000 // 10), head[1])
            case Direction.RIGHT:
                head = ((head[0] + 1) % (1000 // 10), head[1])
        self._stack.insert(0, head)
        self._stack.pop()

    def extend(self):
        # grow the snake by 1 cell
        self._stack.append(tuple(self._stack[-1]))

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, dir: Direction):
        self._direction = dir


class Apple:
    def __init__(self, color: str = "yellow"):
        self._x: int = random.randint(1, 1000 // 10)  # Hardcoded board dimensions
        self._y: int = random.randint(1, 1000 // 10)
        self.color = color

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def coordinates(self) -> tuple[int, int]:
        return (self._x, self._y)


class GameState:
    def __init__(self):
        self._snake = Snake()
        self._apple = Apple()

    @property
    def gameover(self):
        return False

    @property
    def snake(self):
        return self._snake

    @property
    def apple(self):
        return self._apple

    def consume_apple(self):
        self._apple = Apple()
        self.snake.extend()


class GameBoard:
    KEYS = ["w", "a", "s", "d", "Left", "Right", "Up", "Down"]

    def __init__(
        self, parent: tk.Widget, background: str = "black", tile_size: int = 10
    ):
        self.tile_size = tile_size
        self._canvas = tk.Canvas(
            parent,
            # width=parent.winfo_screenwidth(),
            # height=parent.winfo_screenheight(),
            width=1000,  # Hardcoded board dimensions
            height=1000,
            background=background,
        )
        self._canvas.pack()
        self._key = None
        self.state = GameState()

    def set_key_event(self, event):
        logging.warning(event)
        if event.keysym in GameBoard.KEYS:
            self._key = event.keysym

    def render(self):
        # clear the canvas
        self._canvas.delete(tk.ALL)

        # draw the snake's head
        head = self.state.snake._stack[0]
        self._canvas.create_rectangle(
            head[0] * self.tile_size,
            head[1] * self.tile_size,
            head[0] * self.tile_size + self.tile_size,
            head[1] * self.tile_size + self.tile_size,
            fill=self.state.snake.head_color,
        )

        # draw the snake's body
        for cell in self.state.snake._stack[1:]:
            self._canvas.create_rectangle(
                cell[0] * self.tile_size,
                cell[1] * self.tile_size,
                cell[0] * self.tile_size + self.tile_size,
                cell[1] * self.tile_size + self.tile_size,
                fill=self.state.snake.body_color,
            )

        # draw the apple
        # print(self.state.apple.x, self.state.apple.y, self.state.apple.color)
        self._canvas.create_rectangle(
            self.state.apple.x * self.tile_size,
            self.state.apple.y * self.tile_size,
            self.state.apple.x * self.tile_size + self.tile_size,
            self.state.apple.y * self.tile_size + self.tile_size,
            fill=self.state.apple.color,
        )

    def game_loop(self):
        self._canvas.after(200, self.game_loop)

        if not self.state.gameover:
            self.render()
            if self._key:
                match self._key:
                    case "w" | "Up":
                        self.state.snake.direction = Direction.UP
                    case "s" | "Down":
                        self.state.snake.direction = Direction.DOWN
                    case "a" | "Left":
                        self.state.snake.direction = Direction.LEFT
                    case "d" | "Right":
                        self.state.snake.direction = Direction.RIGHT
            self.state.snake.move()
            if self.state.snake.head == self.state.apple.coordinates:
                self.state.consume_apple()


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    board = GameBoard(frame)
    root.bind("<Key>", board.set_key_event)
    board.game_loop()
    root.mainloop()
#
