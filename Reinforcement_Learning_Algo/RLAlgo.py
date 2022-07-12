import random
import json
import os

import dataclasses

@dataclasses.dataclass
class gameState:
    distance: tuple
    position: tuple
    surroundings: str
    food: tuple

curr_dir = os.path.dirname(os.path.abspath(__file__))
q_values_json = curr_dir + "/qvalues.json"


class reinforcement_learning(object):
    def __init__(self, display_width, display_height, block_size):
        
        self.display_width = display_width
        self.epsilon = 0.1
        self.learning_rate = 0.4
        self.discount = .5
        self.display_height = display_height
        self.block_size = block_size
        self.qvalues = self.load_Qvalues()
        self.history = []

        
        self.actions = {
            0:'LEFT',
            1:'RIGHT',
            2:'UP',
            3:'DOWN'
        }

    def act(self, snake, food):
        state = self._get_state(snake, food)

       
        rand = random.uniform(0,1)
        if rand < self.epsilon:
            action_key = random.choices(list(self.actions.keys()))[0]
        else:
            score_states = self.qvalues[self._get_state_current(state)]
            action_key = score_states.index(max(score_states))
        action_val = self.actions[action_key]
        
        self.history.append({
            'state': state,
            'action': action_key
            })
        return action_val

    def save_Qvalues(self, path=q_values_json):
        with open(path, "w") as f:
            json.dump(self.qvalues, f)

    def reset(self):
        self.history = []

    def load_Qvalues(self, path=q_values_json):
        with open(path, "r") as f:
            qvalues = json.load(f)
        return qvalues

   
    
    
    def update_Qvalues(self, reason):
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            if reason: 
                action_history = history[0]['action']
                state_history = history[0]['state']
                
                state_str = self._get_state_current(state_history)
                reward = -1
                self.qvalues[state_str][action_history] = (1-self.learning_rate) * self.qvalues[state_str][action_history] + self.learning_rate * reward # Bellman equation - there is no future state since game is over
                reason = None
            else:
                current_state = h['state'] 
                previous_state = history[i+1]['state'] 
                previous_action = history[i+1]['action'] 
                
                x_previous = current_state.distance[0] 
                y_previous = current_state.distance[1] 

                x_current = previous_state.distance[0] 
                y_current = previous_state.distance[1] 
    
                
                
                if previous_state.food != current_state.food: #
                    reward = 1
                elif (abs(x_current) > abs(x_previous) or abs(y_current) > abs(y_previous)): 
                    reward = 1
                else:
                    reward = -1 # 
                    
                state_str = self._get_state_current(previous_state)
                new_state_str = self._get_state_current(current_state)
                self.qvalues[state_str][previous_action] = (1-self.learning_rate) * (self.qvalues[state_str][previous_action]) + self.learning_rate * (reward + self.discount*max(self.qvalues[new_state_str])) # Bellman equation


    def _get_state(self, snake, food):
        snake_head = snake[0], snake[1]
        x_distance = food[0] - snake_head[0]
        y_distance = food[1] - snake_head[1]

        if x_distance > 0:
            x_position = '1' 
        elif x_distance < 0:
            x_position = '0' 
        else:
            x_position = 'NA' 

        if y_distance > 0:
            y_position = '3' 
        elif y_distance < 0:
            y_position = '2' 
        else:
            y_position = 'NA' 

        sequence = [
            (snake_head[0]-self.block_size, snake_head[1]),   
            (snake_head[0]+self.block_size, snake_head[1]),         
            (snake_head[0], snake_head[1]-self.block_size),
            (snake_head[0], snake_head[1]+self.block_size),
        ]
        
        state_list = []
        for sq in sequence:
            if sq[0] < 0 or sq[1] < 0: 
                state_list.append('1')
            elif sq[0] >= self.display_width or sq[1] >= self.display_height: 
                state_list.append('1')
            elif sq in snake[:-1]:
                state_list.append('1')
            else:
                state_list.append('0')
        surroundings = ''.join(state_list)

        return gameState((x_distance, y_distance), (x_position, y_position), surroundings, food)

    def _get_state_current(self, state):
        return str((state.position[0],state.position[1],state.surroundings))
