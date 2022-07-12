# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 16:48:33 2022

@author: Shubham
"""

"""
Snake Eater
Made with PyGame
"""


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120

from Dijkstras_Algo.dijkstras import dijkstras
from Baseline_Model.baseline import baseline_path_generator
import random
import time
import sys
import pygame
import sys
import os
import psutil
import timeit
SCRIPT_DIR = os.path.dirname(os.path.abspath(
    'E:\Course Content\sem 2\AI\Group Project Codebase\AIGroupProject\Dijkstras_Algo\dijkstras.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))
difficulty = 100

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print("[!] Had {check_errors[1]} errors when initialising game, exiting...")
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
default_snake_pos = [100, 50]
default_snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

default_food_pos = [random.randrange(
    1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
default_food_spawn = True

direction = 'RIGHT'
change_to = direction

default_score = 0


def get_starting_positions():
    snake_start = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    food_position = [random.randrange(
        1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    score = default_score
    return snake_start, snake_body, food_position, score
    # return snake_body, food_position

# Game Over


def game_over(score, game_window):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20, score, game_window)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def game_over_dijkstras(score, game_window, avg_memory_consumed, avg_execution_time):
    print("Average execution time per iteration of the game:", avg_execution_time)
    print("Average memory consumed per game:", avg_memory_consumed)
    print("Score:", score)
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20, score, game_window)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size, score, game_window):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Method to get the appropriate change in direction based on events
# Also the method that will be called using AI implementation
def get_snake_position_change_to(events, change_to):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    return change_to

# Method to make sure the snake cannot move in the opposite direction instantaneously


def get_updated_direction(change_to, direction):
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    return direction


# Method to make sure the snake cannot move in the opposite direction instantaneously


def get_updated_direction_conflict(change_to, direction):
    direction_error = None
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'UP' and direction == 'DOWN':
        direction_error = 'CONFLICT'

    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'DOWN' and direction == 'UP':
        direction_error = 'CONFLICT'

    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'LEFT' and direction == 'RIGHT':
        direction_error = 'CONFLICT'

    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    elif change_to == 'RIGHT' and direction == 'LEFT':
        direction_error = 'CONFLICT'

    return direction, direction_error

# Method to update and return snake_postion


def get_updated_snake_pos(snake_pos, direction):
    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
    return snake_pos


def handle_game_over(snake_body, food_pos, score):
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    return direction, snake_body, food_pos, score, True

# Method to run snake game with iterations for algo such as Genetic and RL


def run_snake_game_with_iterations(change_to, direction,  snake_pos=default_snake_pos,
                                   food_pos=default_food_pos,
                                   snake_body=default_snake_body,
                                   food_spawn=default_food_spawn,
                                   score=default_score):

    pygame.display.set_caption("SCORE: " + str(score))

    pygame.display.update()

    # Main method to override based on AI implementation
    change_to = get_snake_position_change_to(pygame.event.get(), change_to)

    direction = get_updated_direction(change_to, direction)
    snake_pos = get_updated_snake_pos(snake_pos, direction)

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(
            1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(
        food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        return handle_game_over(snake_body, food_pos, score)
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        return handle_game_over(snake_body, food_pos, score)
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            return handle_game_over(snake_body, food_pos, score)

    show_score(1, white, 'consolas', 20, score, game_window)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    return direction, snake_body, food_pos, score, False

# Method to run game manually and link algos for path planning such as ASTAR and DIJKSTRA's algo


def run_snake_game(change_to, direction, snake_pos=default_snake_pos,
                   food_pos=default_food_pos,
                   snake_body=default_snake_body,
                   food_spawn=default_food_spawn,
                   score=default_score):

    change_to = direction

    # Main method to override based on AI implementation
    change_to = get_snake_position_change_to(pygame.event.get(), change_to)

    direction = get_updated_direction(change_to, direction)
    snake_pos = get_updated_snake_pos(snake_pos, direction)

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(
            1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(
        food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over(score, game_window)
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over(score, game_window)
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over(score, game_window)

    show_score(1, white, 'consolas', 20, score, game_window)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)
    return snake_body, food_pos, score


def run_snake_game_dijkstras(change_to, direction, snake_pos=default_snake_pos,
                             food_pos=default_food_pos,
                             snake_body=default_snake_body,
                             food_spawn=default_food_spawn,
                             score=default_score):

    change_to = direction
    game_count = 0
    total_memory_consumed = 0
    avg_memory_consumed = 0
    start_time = timeit.default_timer()
    total_execution_time = 0
    avg_execution_time = 0

    moves = dijkstras(snake_pos, food_pos, frame_size_x, frame_size_y)
    while True:
        # Main method to override based on AI implementation

        # direction = current direction, changeTo = new direction
        # get a stack of moves from snake_pos to food_pos
        # pop the stack to get a new direction each time, update snake position
        # if stack is empty and food_spawn==false, generate new food_pos and new snake_pos
        # run algorithm again to get new set of moves
        # reiterate infinitely

        # change_to = get_snake_position_change_to(pygame.event.get(), change_to)

        # when moves no empty and goal not reached
        if moves and food_spawn:
            change_to = moves.pop(0)

        # corner case, null check handling
        # if no more moves and goal not reached, find path from current position to goal and continue execution
        elif not moves and food_spawn:
            print("out of moves")
            moves = dijkstras(snake_pos, food_pos, frame_size_x, frame_size_y)
            change_to = moves.pop(0)

        # debug statements
        # print(change_to)

        # update current direction and snake position based on current move
        direction, dir_error = get_updated_direction_conflict(
            change_to, direction)

        # logic to handle conflicting directions
        while dir_error == 'CONFLICT':
            print('in conflict')
            if direction == 'UP' or direction == 'DOWN':
                direction = random.choice(['LEFT', 'RIGHT'])
            else:
                direction = random.choice(['UP', 'DOWN'])
            print("Change direction to:", direction)
            snake_pos = get_updated_snake_pos(snake_pos, direction)
            moves = dijkstras(snake_pos, food_pos, frame_size_x, frame_size_y)
            direction, dir_error = get_updated_direction_conflict(
                change_to, direction)

        snake_pos = get_updated_snake_pos(snake_pos, direction)

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        # if goal state achieved, increment score and remove food
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            print("found goal")
            score += 1
            food_spawn = False
        # else do nothing
        else:
            snake_body.pop()

        # Spawning food on the screen after previous goal achieved
        if not food_spawn:
            food_pos = [random.randrange(
                1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            # new path from snake_pos to food_pos after new goal state generated
            moves = dijkstras(snake_pos, food_pos, frame_size_x, frame_size_y)
            # calculate avg memory consumed by process
            game_count += 1
            total_memory_consumed += psutil.Process(
                os.getpid()).memory_info().rss / 1024 ** 2
            avg_memory_consumed = total_memory_consumed/game_count
            # calculate average execution time per game
            total_execution_time += timeit.default_timer() - start_time
            avg_execution_time = total_execution_time/game_count

        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(
            food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over_dijkstras(score, game_window,
                                avg_memory_consumed, avg_execution_time)
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over_dijkstras(score, game_window,
                                avg_memory_consumed, avg_execution_time)
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over_dijkstras(score, game_window,
                                    avg_memory_consumed, avg_execution_time)

        show_score(1, white, 'consolas', 20, score, game_window)

        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)


def run_snake_game_baseline(change_to, direction, snake_pos=default_snake_pos,
                            food_pos=default_food_pos,
                            snake_body=default_snake_body,
                            food_spawn=default_food_spawn,
                            score=default_score):

    change_to = direction

    moves = baseline_path_generator()
    while True:
        if moves and food_spawn:
            change_to = moves.pop(0)

        # update current direction and snake position based on current move
        direction = get_updated_direction(change_to, direction)
        snake_pos = get_updated_snake_pos(snake_pos, direction)

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        # if goal state achieved, increment score and remove food
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            print("found goal")
            score += 1
            food_spawn = False
        # else do nothing
        else:
            snake_body.pop()

        # Spawning food on the screen after previous goal achieved
        if not food_spawn:
            food_pos = [random.randrange(
                1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            # new path from snake_pos to food_pos after new goal state generated
            moves = dijkstras(snake_pos, food_pos, frame_size_x, frame_size_y)
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(
            food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over(score, game_window)
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over(score, game_window)
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score, game_window)

        show_score(1, white, 'consolas', 20, score, game_window)

        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)
