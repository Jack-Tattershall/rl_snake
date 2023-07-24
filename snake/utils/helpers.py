from dataclasses import dataclass
from typing import Union
from enum import Enum, auto
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

class Object(Enum):
    SNAKE_END = -1
    SNAKE_HEAD = 0
    SNAKE_SEG = 1
    APPLE = 2


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    IDLE = auto()


class Difficulty(Enum):
    EASY = 10
    MEDIUM = 30
    HARD = 50


@dataclass
class GameParams:
    screen_width: int
    screen_height: int
    block_size: int
    difficulty: Difficulty
    human: bool


@dataclass
class SnakeStatus:
    is_alive: bool = True
    apple_eaten: bool = True
    direction: Direction = Direction.IDLE


@dataclass
class GameInfo:
    game_params: GameParams
    snake_status: SnakeStatus
    _score: int = -1

    @property
    def score(self) -> int:
        return self._score
    

# Block class to pass in the colour and position
class Block(pygame.sprite.Sprite):
    def __init__(self, object: Object, w_pos: int, h_pos: int, game_info: GameInfo) -> None:
        
        # Inherit from parent class (Sprite) constructor
        super().__init__()

        self.game_info = game_info

        # Get colour, fill surface and set position
        color = (238, 144, 144) if object == Object.APPLE else (144, 238, 144)
        self.surf = pygame.Surface(
            (
                self.game_info.game_params.block_size,
                self.game_info.game_params.block_size,
            )
        )
        self.surf.fill(color=color)
        self.rect = self.surf.get_rect(
            topleft=(
                w_pos,
                h_pos,
            )
        )

    # Move the Block based on user keypress
    def update(self, pressed_keys: Union[Direction, pygame.key.ScancodeWrapper]):

        if pressed_keys[K_UP] or self.game_info.snake_status.direction == Direction.UP:
            self.rect.move_ip(0, -self.game_info.game_params.block_size)
            self.game_info.snake_status.direction = Direction.UP
        if (
            pressed_keys[K_DOWN]
            or self.game_info.snake_status.direction == Direction.DOWN
        ):
            self.rect.move_ip(0, self.game_info.game_params.block_size)
            self.game_info.snake_status.direction = Direction.DOWN

        if (
            pressed_keys[K_LEFT]
            or self.game_info.snake_status.direction == Direction.LEFT
        ):
            self.rect.move_ip(-self.game_info.game_params.block_size, 0)
            self.game_info.snake_status.direction = Direction.LEFT

        if (
            pressed_keys[K_RIGHT]
            or self.game_info.snake_status.direction == Direction.RIGHT
        ):
            self.rect.move_ip(self.game_info.game_params.block_size, 0)
            self.game_info.snake_status.direction = Direction.RIGHT

        return self.game_info.snake_status.direction

    # Check if block has collided with another
    def check_collision(self, block) -> bool:

        collision = False
        if (
            self.rect.left == block.rect.left
            and self.rect.right == block.rect.right
            and self.rect.top == block.rect.top
            and self.rect.bottom == block.rect.bottom
        ):
            collision = True
            return collision

    # Check if block off screen
    def off_screen(self) -> bool:

        return (
            True
            if (
                self.rect.bottom <= 0
                or self.rect.top >= self.game_info.game_params.screen_height
                or self.rect.right <= 0
                or self.rect.left >= self.game_info.game_params.screen_width
            )
            else False
        )
