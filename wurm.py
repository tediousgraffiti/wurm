import tkinter as tk
from tkinter import ttk
import random
from enum import Enum

# Example 1:
# root = tk.Tk()
# frame = tk.Frame(root)
# canvas = tk.Canvas(frame, width=900, height=900, background="yellow")
# frame.pack()
# canvas.grid()
# canvas.create_rectangle(10 * 20, 10 * 20, 10 * 20 + 10, 10 * 20 + 10, fill="red")
# root.mainloop()


class Direction(Enum):
    UP = "w"
    DOWN = "s"
    LEFT = "a"
    RIGHT = "d"


class Snake:
    def __init__(self, head_color: str = "red", body_color: str = "green"):
        self._stack = [(20, 20), (20, 21), (20, 22)]
        self.length = len(self._stack)  # this should be a property
        self.direction = Direction.DOWN
        self.head_color = head_color
        self.body_color = body_color

    def move(self):
        match self.direction:
            case Direction.DOWN:
                pass
            case Direction.UP:
                pass
            case Direction.LEFT:
                pass
            case Direction.RIGHT:
                pass
            case _:
                pass

    def eat_apple(self):
        # grow the snake by 1 cell
        pass


class Apple:
    def __init__(self, color: str = "black"):
        self._x: int = 89  # Hardcoded board dimensions
        self._y: int = 89
        self.color = color

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y


class GameState:
    def __init__(self):
        self._snake = Snake()
        self._apple = Apple()

    @property
    def gameover(self):
        pass

    @property
    def snake(self):
        return self._snake

    @property
    def apple(self):
        return self._apple


class GameBoard:
    def __init__(
        self, parent: tk.Widget, background: str = "yellow", tile_size: int = 10
    ):
        self.tile_size = tile_size
        self._canvas = tk.Canvas(
            parent,
            # width=parent.winfo_screenwidth(),
            # height=parent.winfo_screenheight(),
            width=900,  # Hardcoded board dimensions
            height=900,
            background=background,
        )
        self._canvas.pack()

    def render(self, state: GameState):
        # clear the canvas
        self._canvas.delete(tk.ALL)

        # draw the snake's head
        head = state.snake._stack[0]
        self._canvas.create_rectangle(
            head[0] * self.tile_size,
            head[1] * self.tile_size,
            head[0] * self.tile_size + self.tile_size,
            head[1] * self.tile_size + self.tile_size,
            fill=state.snake.head_color,
        )

        # draw the snake's body
        for cell in state.snake._stack[1:]:
            self._canvas.create_rectangle(
                cell[0] * self.tile_size,
                cell[1] * self.tile_size,
                cell[0] * self.tile_size + self.tile_size,
                cell[1] * self.tile_size + self.tile_size,
                fill=state.snake.body_color,
            )

        # draw the apple
        print(state.apple.x, state.apple.y, state.apple.color)
        self._canvas.create_rectangle(
            state.apple.x * self.tile_size,
            state.apple.y * self.tile_size,
            state.apple.x * self.tile_size + self.tile_size,
            state.apple.y * self.tile_size + self.tile_size,
            fill=state.apple.color,
        )


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    # Create board
    board = GameBoard(frame)
    # Initial State
    state = GameState()
    # Render the board
    board.render(state)

    # Enter GameLoop...

    root.mainloop()
#
