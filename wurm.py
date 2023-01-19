import tkinter as tk
from tkinter import ttk
import random
from enum import Enum
import logging


# TODO:
# 1. no walking back through self (x)
# 2. collision detection and gameover (x)
# 3. factor out App from GameBoard (x)
# 4. fix hardcoded board dimensions
# 5. Add scoring, hud
# 6. add additional configuration options (e.g. tick speed, starting length, toggle walls) and CLI
# 7. menu and restart
# 8. Bugsquash
#    - what happens if the apple is placed inside the snake's body?
#    - make sure apple is placed within display area?


class Direction(Enum):
    UP = "w"
    DOWN = "s"
    LEFT = "a"
    RIGHT = "d"


class Snake:
    OPPOSITE_DIRECTIONS = [
        {Direction.UP, Direction.DOWN},
        {Direction.LEFT, Direction.RIGHT},
    ]

    def __init__(self, head_color: str = "red", body_color: str = "green"):
        self._stack = [(20, 20), (20, 21), (20, 22), (20, 23)]
        self._direction = Direction.UP
        self.head_color = head_color
        self.body_color = body_color

    @property
    def head(self):
        return self._stack[0]

    @property
    def tail(self):
        return self._stack[1:]

    @property
    def length(self):
        return len(self._stack)

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
        # grow the snake by 1 cell by just duping the end of the tail
        self._stack.append(tuple(self._stack[-1]))

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction: Direction):
        if {self.direction, new_direction} not in Snake.OPPOSITE_DIRECTIONS:
            self._direction = new_direction

    def is_self_intersecting(self):
        return self.head in self.tail


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
        return self.snake.is_self_intersecting()

    @property
    def snake(self):
        return self._snake

    @property
    def apple(self):
        return self._apple

    def consume_apple(self):
        self._apple = Apple()
        logging.warning(f"{self._apple.coordinates}")
        self.snake.extend()


class GameBoard(tk.Canvas):
    def __init__(
        self,
        *args,
        tile_size: int = 10,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.tile_size = tile_size
        # self._canvas = tk.Canvas(
        #     parent,
        #     # width=parent.winfo_screenwidth(),
        #     # height=parent.winfo_screenheight(),
        #     width=1000,  # Hardcoded board dimensions
        #     height=1000,
        #     background=background,
        # )
        # self._canvas.pack()

    def render(self, state):
        # clear the canvas
        self.delete(tk.ALL)

        # draw the snake's head
        head = state.snake._stack[0]
        self.create_rectangle(
            head[0] * self.tile_size,
            head[1] * self.tile_size,
            head[0] * self.tile_size + self.tile_size,
            head[1] * self.tile_size + self.tile_size,
            fill=state.snake.head_color,
        )

        # draw the snake's body
        for cell in state.snake._stack[1:]:
            self.create_rectangle(
                cell[0] * self.tile_size,
                cell[1] * self.tile_size,
                cell[0] * self.tile_size + self.tile_size,
                cell[1] * self.tile_size + self.tile_size,
                fill=state.snake.body_color,
            )

        # draw the apple
        # print(self.state.apple.x, self.state.apple.y, self.state.apple.color)
        self.create_rectangle(
            state.apple.x * self.tile_size,
            state.apple.y * self.tile_size,
            state.apple.x * self.tile_size + self.tile_size,
            state.apple.y * self.tile_size + self.tile_size,
            fill=state.apple.color,
        )


class App(tk.Tk):
    KEYS = ["w", "a", "s", "d", "Left", "Right", "Up", "Down"]

    def __init__(
        self,
        screenName=None,
        baseName=None,
        className="Tk",
        usetk=True,
        sync=False,
        use=None,
    ):
        tk.Tk.__init__(self, screenName, baseName, className, usetk, sync, use)
        self._frame = tk.Frame(self)
        self._frame.pack()
        self.state = GameState()
        self.board = GameBoard(self._frame, width=1000, height=1000, background="black")
        self.board.pack()
        self._key = None
        self.bind("<Key>", self.set_key_event)

    def set_key_event(self, event):
        # logging.warning(event)
        if event.keysym in App.KEYS:
            self._key = event.keysym

    def game_loop(self):
        if not self.state.gameover:
            self.board.render(self.state)
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
            self.after(200, self.game_loop)
        else:
            logging.error("YOU DIED")

    def mainloop(self, n=0):
        self.game_loop()
        tk.Tk.mainloop(self, n)


if __name__ == "__main__":
    # root = tk.Tk()
    # frame = tk.Frame(root)
    # frame.pack()
    # board = GameBoard(frame)
    # root.bind("<Key>", board.set_key_event)
    # board.game_loop()
    # root.mainloop()
    App().mainloop()
#
