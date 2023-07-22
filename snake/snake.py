from typing import List
import pygame
from random import randint
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from utils.helpers import (
    Object,
    GameInfo, 
    Direction,
    Difficulty,
    GameParams,
    SnakeStatus,
    Block
)

class SnakeGame:
    def __init__(self, game_params: GameParams) -> None:

        self.game_info = GameInfo(game_params, snake_status=SnakeStatus())

    def _init_pygame(self) -> None:

        pygame.init()

        screen = pygame.display.set_mode(
            (
                self.game_info.game_params.screen_width,
                self.game_info.game_params.screen_height,
            )
        )
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Comic Sans MS", 30)

        return screen, clock, font

    def _spawn_apple(self) -> Block:

        w_pos = (
            randint(
                0,
                int(
                    self.game_info.game_params.screen_width
                    / self.game_info.game_params.block_size
                )
                - 1,
            )
            * self.game_info.game_params.block_size
        )
        h_pos = (
            randint(
                0,
                int(
                    self.game_info.game_params.screen_height
                    / self.game_info.game_params.block_size
                )
                - 1,
            )
            * self.game_info.game_params.block_size
        )

        apple = Block(
            Object.APPLE,
            w_pos,
            h_pos,
            self.game_info,
        )

        return apple

    def _spawn_snake_seg(self, snake: List[Block], w_pos: int, h_pos: int) -> List[Block]:

        snake_seg = Block(
            Object.SNAKE_SEG,
            w_pos,
            h_pos,
            self.game_info,
        )
        snake.append(snake_seg)

        return snake

    def _articulate_snake(self, snake: List[Block]) -> List[Block]:

        w_pos = snake[Object.SNAKE_HEAD.value].rect.left
        h_pos = snake[Object.SNAKE_HEAD.value].rect.top
        snake_seg = Block(
            Object.SNAKE_SEG,
            w_pos,
            h_pos,
            self.game_info,
        )
        snake.insert(Object.SNAKE_HEAD.value, snake_seg)
        snake.pop(Object.SNAKE_END.value)

        return snake

    def play(self, action: Direction = Direction.IDLE) -> None:

        # Initialise pygame, create screen and create clock
        screen, clock, font = self._init_pygame()

        # Create snake
        snake = []
        is_start = True

        while True:

            # Look at events
            is_running = True
            for event in pygame.event.get():

                # Available user requests to terminate game
                if (
                    event.type == KEYDOWN
                    and event.key == K_ESCAPE
                    or event.type == QUIT
                ):

                    is_running = False

            # Terminate if user requests
            if not is_running:
                break

            # Clear screen
            screen.fill((0, 0, 0))

            # Place apple
            if self.game_info.snake_status.apple_eaten:

                apple = self._spawn_apple()

                # Place snake segment
                w_pos = (
                    (self.game_info.game_params.screen_width//2)
                    if is_start
                    else snake[Object.SNAKE_END.value].rect.left
                )
                h_pos = (
                    (self.game_info.game_params.screen_height//2)
                    if is_start
                    else snake[Object.SNAKE_END.value].rect.top
                )
                snake = self._spawn_snake_seg(snake, w_pos=w_pos, h_pos=h_pos)
                is_start = False

                # Increment game score
                self.game_info._score += 1

                self.game_info.snake_status.apple_eaten = False

            # Articulate snake
            snake = self._articulate_snake(snake)

            # Get user input
            if self.game_info.game_params.human:
                user_input = pygame.key.get_pressed()
                snake[Object.SNAKE_HEAD.value].update(user_input)
            else:
                self.game_info.snake_status.direction = action

            # Check if snake has eaten apple
            if snake[Object.SNAKE_HEAD.value].check_collision(apple):
                self.game_info.snake_status.apple_eaten = True

            # Check if snake has eaten tail
            for snake_seg in snake[Object.SNAKE_SEG.value :]:
                if snake[Object.SNAKE_HEAD.value].check_collision(snake_seg):
                    self.game_info.snake_status.is_alive = False
                    break

            # Check if snake is off screen
            if snake[Object.SNAKE_HEAD.value].off_screen():
                self.game_info.snake_status.is_alive = False

            # Terminate if snake not alive
            if not self.game_info.snake_status.is_alive:
                break

            # Display snake
            for snake_seg in snake:
                screen.blit(snake_seg.surf, snake_seg.rect)

            # Display apple
            screen.blit(apple.surf, apple.rect)

            # Display score
            text = font.render(f"Score: {self.game_info.score}", False, (255, 0, 0))
            screen.blit(
                text,
                text.get_rect(
                    center=(
                        screen.get_rect().centerx,
                        screen.get_rect().centery
                        - (self.game_info.game_params.block_size * 13),
                    )
                ),
            )

            # Render display
            pygame.display.flip()
            clock.tick(self.game_info.game_params.difficulty.value)


if __name__ == "__main__":

    snake_game = SnakeGame(
        GameParams(
            screen_width=800,
            screen_height=600,
            block_size=20,
            difficulty=Difficulty.EASY,
            human=True,
        )
    )
    snake_game.play()

    print(f"You scored: {snake_game.game_info.score}")

