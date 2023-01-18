# Notes

## Implementation Outline

* App is
  * a display frame
  * a game board in that display frame that knows how to render the current game state
  * a game state that includes the current snake and apple and game-over conditions
  * a gameloop that handles keypress events, updates the game state and triggers the game board to rerender every tick
  * a settings object, including any useful keybindings, font, colors, game options, etc.

## Flow Outline

* initialize the gameloop
  * initialize a fixed size game board
    * wrap the canvas class or compose?
    * store background color
  * initialize the snake (default length, position, direction, and speed)
  * create an apple and place it randomly
* run the gameloop (the tk mainloop is a container for running the gameloop)
  * draw the gameboard
  * read keys
  * if input:
    * in wasd/arrows, update snake.direction to match input key
    * ctrl+r, reset the gameloop
  * snake.move()
    * update snake head and body coordinates according to current position direction and speed
  * detect_collisions()
    * if snake collides with apple, snake.eat(apple) && place new apple
    * if snake collides with self, game_over

## Free notes

* Seems like GameState depends on GameBoard and vice-versa?

## Example Implementations

```python
from tkinter import *
import random
from typing import List


class Apple:
    def __init__(self):
        self.__x = random.randint(1, App.BOARD_WIDTH - 2)
        self.__y = random.randint(1, App.BOARD_HEIGHT - 2)

    def create_new_apple(self) -> None:
        self.__x = random.randint(1, App.BOARD_WIDTH - 2)
        self.__y = random.randint(1, App.BOARD_HEIGHT - 2)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y


class Snake:

    KEYS = ["w", "a", "s", "d"]
    MAP_KEY_OPP = {"w": "s", "a": "d", "s": "w", "d": "a"}

    def __init__(self, apple):
        self.__apple = apple
        self.__x = [20, 20, 20]
        self.__y = [20, 21, 22]
        self.__length = 3
        self.__key_current = "w"
        self.__key_last = self.__key_current
        self.__points = 0

    def move(self) -> None:  # move and change direction with wasd

        self.__key_last = self.__key_current

        for i in range(self.length - 1, 0, -1):
            self.__x[i] = self.__x[i - 1]
            self.__y[i] = self.__y[i - 1]

        if self.__key_current == "w":
            self.__y[0] = self.__y[0] - 1

        elif self.__key_current == "s":
            self.__y[0] = self.__y[0] + 1

        elif self.__key_current == "a":
            self.__x[0] = self.__x[0] - 1

        elif self.__key_current == "d":
            self.__x[0] = self.__x[0] + 1

        self.eat_apple()

    def eat_apple(self) -> None:

        if self.__x[0] == self.__apple.x and self.__y[0] == self.__apple.y:

            self.__length = self.__length + 1

            x = self.__x[len(self.__x) - 1]  # snake grows
            y = self.__y[len(self.__y) - 1]
            self.__x.append(x + 1)
            self.__y.append(y)

            self.__points = self.__points + 1
            self.__apple.create_new_apple()

    @property
    def gameover(self) -> bool:

        for i in range(1, self.length, 1):

            if self.__y[0] == self.__y[i] and self.__x[0] == self.__x[i]:
                return True  # snake ate itself

        if (
            self.__x[0] < 1
            or self.__x[0] >= App.BOARD_WIDTH - 1
            or self.__y[0] < 1
            or self.__y[0] >= App.BOARD_HEIGHT - 1
        ):
            return True  # snake out of bounds

        return False

    def set_key_event(self, event: Event) -> None:

        if (
            event.char in Snake.KEYS
            and event.char != Snake.MAP_KEY_OPP[self.__key_last]
        ):
            self.__key_current = event.char

    @property
    def x(self) -> List[int]:
        return self.__x.copy()

    @property
    def y(self) -> List[int]:
        return self.__y.copy()

    @property
    def length(self) -> int:
        return self.__length

    @property
    def points(self) -> int:
        return self.__points


class App(Tk):

    BOARD_WIDTH = 30
    BOARD_HEIGHT = 30
    TILE_SIZE = 10

    COLOR_BACKGROUND = "yellow"
    COLOR_SNAKE_HEAD = "red"
    COLOR_SNAKE_BODY = "blue"
    COLOR_APPLE = "green"
    COLOR_FONT = "darkblue"
    FONT = "Times 20 italic bold"
    FONT_DISTANCE = 25

    TEXT_TITLE = "Snake"
    TEXT_GAMEOVER = "GameOver!"
    TEXT_POINTS = "Points: "

    TICK_RATE = 200  # in ms

    def __init__(
        self, screenName=None, baseName=None, className="Tk", useTk=1, sync=0, use=None
    ):
        Tk.__init__(self, screenName, baseName, className, useTk, sync, use)

        self.__apple = Apple()
        self.__snake = Snake(self.__apple)

        self.__canvas = Canvas(
            self,
            width=App.BOARD_WIDTH * App.TILE_SIZE,
            height=App.BOARD_HEIGHT * App.TILE_SIZE,
        )
        self.__canvas.pack()
        self.__canvas.configure(background=App.COLOR_BACKGROUND)

        self.title(App.TEXT_TITLE)
        self.bind("<KeyPress>", self.__snake.set_key_event)

    def mainloop(self, n=0):
        self.__gameloop()
        Tk.mainloop(self, n)

    def __gameloop(self):

        self.after(App.TICK_RATE, self.__gameloop)
        self.__canvas.delete(ALL)

        if not self.__snake.gameover:

            self.__snake.move()

            x = self.__snake.x
            y = self.__snake.y

            self.__canvas.create_rectangle(
                x[0] * App.TILE_SIZE,
                y[0] * App.TILE_SIZE,
                x[0] * App.TILE_SIZE + App.TILE_SIZE,
                y[0] * App.TILE_SIZE + App.TILE_SIZE,
                fill=App.COLOR_SNAKE_HEAD,
            )  # Head

            for i in range(1, self.__snake.length, 1):
                self.__canvas.create_rectangle(
                    x[i] * App.TILE_SIZE,
                    y[i] * App.TILE_SIZE,
                    x[i] * App.TILE_SIZE + App.TILE_SIZE,
                    y[i] * App.TILE_SIZE + App.TILE_SIZE,
                    fill=App.COLOR_SNAKE_BODY,
                )  # Body

            self.__canvas.create_rectangle(
                self.__apple.x * App.TILE_SIZE,
                self.__apple.y * App.TILE_SIZE,
                self.__apple.x * App.TILE_SIZE + App.TILE_SIZE,
                self.__apple.y * App.TILE_SIZE + App.TILE_SIZE,
                fill=App.COLOR_APPLE,
            )  # Apple

        else:  # GameOver Message
            x = App.BOARD_WIDTH * App.TILE_SIZE / 2  # x coordinate of screen center
            y = App.BOARD_HEIGHT * App.TILE_SIZE / 2  # y coordinate of screen center
            self.__canvas.create_text(
                x,
                y - App.FONT_DISTANCE,
                fill=App.COLOR_FONT,
                font=App.FONT,
                text=App.TEXT_GAMEOVER,
            )
            self.__canvas.create_text(
                x,
                y + App.FONT_DISTANCE,
                fill=App.COLOR_FONT,
                font=App.FONT,
                text=App.TEXT_POINTS + str(self.__snake.points),
            )


if __name__ == "__main__":
    App().mainloop()
```
