#!/usr/bin/python3
import random

def random_walk_yolo(): 
    input('ready')
    return random.choice(['right','left','forward'])
    

grid_length = int(input('ready'))
while True:
    desired_move = random_walk_yolo()
    #print(desired_move)
    print("forward")
