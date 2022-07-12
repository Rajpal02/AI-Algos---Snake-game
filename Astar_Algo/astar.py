from queue import PriorityQueue
from .snake_prop import *

## Class to get distance from goal state using astar
class AStar:
    def __init__(self):
        self.moves = [
            "RIGHT",
            "LEFT",
            "UP",
            "DOWN"
        ]
        self.moves_invalid = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        self.number_of_moves = 0
    
    ## Method to determine if the snake body is colliding with itself
    def is_snake_body_touching(self, snakeHeadPos, snake_pos):
        return any([body.snake_position == snakeHeadPos for body in snake_pos.body[: -1]])

    ## Method to generate and return the manahttan distance
    def get_manhattan_distance(self, food_coordinates, snake_top, snake_pos):
        queue_for_distance = PriorityQueue()
        self.number_of_moves += 1

        for path in self.moves:
            pos_x = None
            pos_y = None
            food_coordinates_x = food_coordinates.pos_x
            food_coordinates_y = food_coordinates.pos_y

            if path == "UP":
                pos_x = snake_top.pos_x
                pos_y = snake_top.pos_y - 10

            elif path == "DOWN":
                pos_x = snake_top.pos_x
                pos_y = snake_top.pos_y + 10

            elif path == "RIGHT":
                pos_x = snake_top.pos_x + 10
                pos_y = snake_top.pos_y

            elif path == "LEFT":
                pos_x = snake_top.pos_x - 10
                pos_y = snake_top.pos_y

            if self.is_snake_body_touching((pos_x, pos_y), snake_pos):
                continue

            if (pos_x>710 or pos_y>470):
                continue

            cost = self.number_of_moves
            heuristic_cost = abs(pos_x - food_coordinates_x) + abs(pos_y - food_coordinates_y)
            actual_cost = cost + heuristic_cost

            queue_for_distance.put((actual_cost, path))

        return queue_for_distance

    ## Method to return next step for every iteration
    def get_next_step(self, food_coordinates, snake_pos):
        if snake_pos.snake_top.pos_x == food_coordinates.pos_x and snake_pos.snake_top.pos_y == food_coordinates.pos_y:
            self.number_of_moves = 0
            return snake_pos.direction

        actual_distance_list = self.get_manhattan_distance(food_coordinates, snake_pos.snake_top, snake_pos)

        if actual_distance_list.qsize() == 0:
            return snake_pos.direction

        return actual_distance_list.get()[1]
