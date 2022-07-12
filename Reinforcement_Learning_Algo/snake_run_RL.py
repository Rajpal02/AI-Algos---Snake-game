from .RLAlgo import reinforcement_learning
import sys
sys.path.insert(1, '../')
import snake_game
import pygame

def run_rl_algo(total_game_count = 120):
    learner = reinforcement_learning(snake_game.frame_size_x, snake_game.frame_size_y, 10)
    game_count = 1 
    while (game_count <= total_game_count):
        pygame.init()
        snake_start, snake_body, food_position, score = snake_game.get_starting_positions()
        direction = "RIGHT"
        learner.reset() 
        
        moves = 1
        while(moves <=2500):
            action = learner.act(snake_start, food_position)

            direction, snake_body, food_position, score, has_snake_collided = snake_game.run_snake_game_with_iterations(action, direction, snake_start,food_position,snake_body,True,score )
            moves = moves + 1
            if (has_snake_collided == True):
                print("---------------------------")
                break
        
        learner.update_Qvalues("dead")
        print("score",score)
        print("game count",game_count)
        game_count = game_count + 1

def main():
   run_rl_algo()

if __name__ == "__main__":
    main()

            