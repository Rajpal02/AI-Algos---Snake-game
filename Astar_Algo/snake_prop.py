## Class to maintain the snake running logic and invalid moves
class SnakeBody(object):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    @property
    def snake_position(self):
        return self.pos_x, self.pos_y

## Class to maintain the food position
class SnakeFood(object):
    def __init__(self, snake_pos, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.snake_pos = snake_pos


class Snake(object):
    def __init__(self, pos_x, pos_y, snake_body):
        self.body = list()
        snake_len = len(snake_body)
        for i in range(snake_len-1,0,-1):
            self.body.append(SnakeBody(snake_body[i][0], snake_body[i][1]))

        self.body.append(SnakeBody(pos_x, pos_y))
        self.direction = "RIGHT"
        self.last = (pos_x, pos_y)

        self.moves_invalid = {
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
            "UP": "DOWN",
            "DOWN": "UP",
        }
    ## Snake head property
    @property
    def snake_top(self):
        return self.body[-1]
