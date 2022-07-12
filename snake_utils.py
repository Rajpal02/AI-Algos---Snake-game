import numpy as np
import math

## get blocked directions for the snake from the snake_body
def get_blocked_directions(snake_body):
    current_vector_for_direction = np.array(snake_body[0]) - np.array(snake_body[1])

    left_direction_vector = np.array([current_vector_for_direction[1], -current_vector_for_direction[0]])
    right_direction_vector = np.array([-current_vector_for_direction[1], current_vector_for_direction[0]])

    is_blocked_front_present = is_blocked_direction_for_snake(snake_body, current_vector_for_direction)
    is_blocked_left_present = is_blocked_direction_for_snake(snake_body, left_direction_vector)
    is_blocked_right_present = is_blocked_direction_for_snake(snake_body, right_direction_vector)

    return is_blocked_front_present, is_blocked_left_present, is_blocked_right_present


## returns if the direction is blocked for the snake body
def is_blocked_direction_for_snake(snake_body, current_vector_for_direction):
    next_step = snake_body[0] + current_vector_for_direction
    if is_colliding_with_boundaries(next_step) == 1 or is_colliding_with_self(next_step.tolist(), snake_body) == 1:
        return 1
    else:
        return 0

## checks if the snake collides with the boundries
def is_colliding_with_boundaries(snake_start_position):
    if snake_start_position[0] >= 720 or snake_start_position[0] < 0 or snake_start_position[1] >= 480 or snake_start_position[1] < 0:
        return 1
    else:
        return 0

## checks if the snake is colliding with self
def is_colliding_with_self(snake_start, snake_body):
    if snake_start in snake_body[1:]:
        return 1
    else:
        return 0

## Returns the tan (angle) of the snake with the food position
def get_food_and_direction_vectors(snake_body, food_position):
    food_direction_vector = np.array(food_position) - np.array(snake_body[0])
    snake_vector_for_direction = np.array(snake_body[0]) - np.array(snake_body[1])

    food_direction_vector_norm = np.linalg.norm(food_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_vector_for_direction)
    if food_direction_vector_norm == 0:
        food_direction_vector_norm = 10

    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    food_direction_vector_normalized = food_direction_vector / food_direction_vector_norm
    snake_normalised_direction_vector = snake_vector_for_direction / norm_of_snake_direction_vector
    return food_direction_vector_normalized, snake_normalised_direction_vector