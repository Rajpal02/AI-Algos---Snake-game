from .astar import AStar
from .snake_prop import *

import sys
sys.path.insert(1, '../')
import snake_game

def run_snake():
    snake_start, snake_body, food_position, score = snake_game.get_starting_positions()
    astar = AStar()

    while True:
        snake = Snake(snake_body[0][0], snake_body[0][1], snake_body)
        food = SnakeFood(snake,food_position[0],food_position[1])
        event = astar.get_next_step(food, snake)           
        snake_body, food_position, score = snake_game.run_snake_game(event, event, snake_start, food_position, snake_body, True, score)

def main():
    run_snake()

if __name__ == "__main__":
    main()
