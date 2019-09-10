#!/usr/bin/python3
import random

cycle_count = 0
first_left = True
direction = 'left'

def init_vars():
    grid_length = int(input('ready'))
    grid = [['x'] * grid_length for i in range(grid_length)]
    return grid_length, grid

def random_walk_yolo(): 
    input('ready')
    return random.choice(['right','left','forward'])

def squeeze(grid_length,grid):
    global cycle_count
    global first_left
    global direction
    state = input('ready')
    parsed_state = state.split(',')
    if cycle_count < grid_length - 1:
        cycle_count += 1
        return 'forward',grid
    elif cycle_count == grid_length:
        cycle_count += 1
        if direction == 'left':
            return 'left',grid
        else:
            return 'right',grid
    else:
        cycle_count = 0
        if direction == 'left':
            direction = 'right'
            return 'left',grid
        else:
            direction = 'left'
            return 'right',grid
    
    
def random_walk_no_crash(grid,grid_lenth): #with self worth this time
    state = input('ready')
    parsed_state = state.split(',')
    current_dir = parsed_state[0]
    current_x = int(parsed_state[1])
    current_y = int(parsed_state[2])
    grid[current_y][current_x] = 'M'
    op_x = int(parsed_state[4])
    op_y = int(parsed_state[5])
    grid[op_y][op_x] ='O'
    desired_x = current_x
    desired_y = current_y
    posible_moves = ['right','left','forward']
    while len(posible_moves) > 0:
            desired_move = random.choice(posible_moves)
            desired_x = current_x
            desired_y = current_y
            if current_dir == 'n':
                if desired_move == 'right':
                    desired_x = current_x + 1
                elif desired_move == 'left':
                    desired_x = current_x - 1
                else:
                    desired_y = current_y - 1
            elif current_dir == 's':
                if desired_move == 'right':
                    desired_x = current_x - 1
                elif desired_move == 'left':
                    desired_x = current_x + 1
                else:
                    desired_y = current_y + 1
            elif current_dir == 'e':
                if desired_move == 'right':
                    desired_y= current_y + 1
                elif desired_move == 'left':
                    desired_y = current_y - 1
                else:
                    desired_x = current_x + 1   
            else: 
                if desired_move == 'right':
                    desired_y = current_y - 1
                elif desired_move == 'left':
                    desired_y = current_y + 1
                else:
                    desired_x = current_x - 1
            if(desired_x < 0 or desired_x > grid_length - 1 or desired_y < 0 or desired_y > grid_length - 1):
                posible_moves.remove(desired_move)
            elif grid[desired_y][desired_x] != 'x':
                posible_moves.remove(desired_move)
            else:
                return desired_move,grid
    return 'forward',grid


grid_length, grid = init_vars()
while True:
    #desired_move,grid = random_walk_no_crash(grid,grid_length)
    #print(desired_move)
    input("ready")
    print("forward")

    
