import snake_game
import random
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(
    'E:\Course Content\sem 2\AI\Group Project Codebase\AIGroupProject\snake_game.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def baseline_path_generator():
    path = []
    dirs = ['LEFT', 'RIGHT', 'UP', 'DOWN']
    for i in range(2500):
        path.append(random.choice(dirs))
    return path
