import numpy as np
from .genetic_neural_net import *

## Code to import file at runtime from separate root folder
import sys
sys.path.insert(1, '../')
import snake_game
import snake_utils

def get_button_direction(direction):
    button_direction = "LEFT"
    if direction.tolist() == [10, 0]:
        button_direction = "RIGHT"
    elif direction.tolist() == [-10, 0]:
        button_direction = "LEFT"
    elif direction.tolist() == [0, 10]:
        button_direction = "DOWN"
    else:
        button_direction = "UP"

    return button_direction

def run_snake_with_genetic(weights):
    total_steps_per_game = 2500
    maximum_score = 0

    snake_start, snake_body, food_position, score = snake_game.get_starting_positions()
    for _ in  range(total_steps_per_game):
        is_front_blocked, is_left_blocked, is_right_blocked = snake_utils.get_blocked_directions(
            snake_body)

        food_direction_vector_normalized, snake_direction_vector_normalized = snake_utils.get_food_and_direction_vectors(
            snake_body, food_position)

        predicted_direction = np.argmax(np.array(feed_forward(np.array(
            [is_left_blocked, is_front_blocked, is_right_blocked, food_direction_vector_normalized[0],
                snake_direction_vector_normalized[0], food_direction_vector_normalized[1],
                snake_direction_vector_normalized[1]]).reshape(-1, 7), weights))) - 1

        updated_direction = np.array(snake_body[0]) - np.array(snake_body[1])
        if predicted_direction == -1:
            updated_direction = np.array([updated_direction[1], -updated_direction[0]])
        if predicted_direction == 1:
            updated_direction = np.array([-updated_direction[1], updated_direction[0]])

        button_direction = get_button_direction(updated_direction)

        dir, snake_body, food_position, score, has_snake_collided = snake_game.run_snake_game_with_iterations(button_direction, button_direction, snake_start, food_position, snake_body, True, score)
        
        if has_snake_collided:
            break

        if score > maximum_score:
            maximum_score = score
    return maximum_score
