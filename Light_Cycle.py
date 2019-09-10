import pexpect #will need to be installed for this to work
import pexpect.popen_spawn
import sys
import random
import time
import pandas 
import os
import pprint
if len(sys.argv) == 3:
    red_player_file = sys.argv[1]
    blue_player_file = sys.argv[2]
elif len(sys.argv) == 4:
    red_player_file = sys.argv[1]
    blue_player_file = sys.argv[2]
    grid_length = int(sys.argv[3])
else:
    red_player_file = 'test_red.py' #hard coded files to be used as bike controls
    blue_player_file = 'test_blue.py'
    grid_length = 10

grid = [['.'] * grid_length for i in range(grid_length)] #first value in 2d list is row then col or y then x


class Bike:
    def __init__(self, start_x,start_y,direction,process,file_name,time_out = 1):
        self.__pos_x = start_x          #cars x position in grid
        self.__pos_y = start_y          #cars y position in grid
        self.__future_x = start_x       #where x position of where car wants to move which is checked to see if valid 
        self.__future_y = start_y       #where y position of where car wants to move which is checked to see if valid 
        self.__direction = direction    #the direction car is faceing 
        self.__process = process        #pexpect object that contains chile process
        self.__file_name = file_name    #name of python file related to this cars ai
        self.__time_out = time_out      #how lone the process.expect() command is going to wait for responce before giving up
        self.__crashed = False          #has the car crashed?
        self.__timeout = False          #has the car timed out a process.expect() command?
        self.__next_move = ''           #does the car want to go forward, left, or right

    def get_next_move(self):
        return self.__next_move 

    def get_car_state_string(self): #returns direction,x_pos,y_pos in one string so it can be sent to the oppent 
        return str(self.__direction) +','+ str(self.__pos_x)+','+ str(self.__pos_y)

    def change_pos(self):
        self.__pos_x = self.__future_x
        self.__pos_y = self.__future_y

    def state_transaction(self,grid,enemy_state_string): #sends car state string and oppents state string to process and expects next move to be returned
        i = self.__process.expect(['ready',pexpect.TIMEOUT,pexpect.EOF],timeout = self.__time_out)

        if i == 1:
            print('Time out on ' + self.__file_name +'. Ready signal not sent')
            self.__timeout = True
            sys.exit(0)
        elif i == 2:
            print('Program ended in file ' + self.__file_name + ' : Program needs to not end on its own and needs a correct path to file. Try useing an infinite loop and make sure your client doesnt crash')
            sys.exit(0)
        out_put = self.__direction+','+str(self.__pos_x)+','+str(self.__pos_y)+','+enemy_state_string

        number_bytes = self.__process.sendline(out_put)

        i = self.__process.expect(['left','right','forward',pexpect.TIMEOUT,pexpect.EOF],timeout = self.__time_out)

        if i == 0:
            self.__next_move = 'left'
        elif i == 1:
            self.__next_move = 'right'
        elif i == 2:
            self.__next_move = 'forward'
        elif i == 3:
            print('Time out on ' + self.__file_name +'. No direction information sent')
            self.__timeout = True
            sys.exit(0)
        elif i == 4:
            print('Program ended in file ' + self.__file_name + ' : Program needs to not end on its own and needs a correct path to file. Try useing an infinite loop and make sure your client doesnt crash')
            sys.exit(0)
        return self.__pos_x, self.__pos_y

    def update_position(self): #translates the next_move direction to a possition in the grid
        global grid
        if self.__direction == 'n':
            if self.__next_move == 'right':
                self.__direction = 'e'
                self.__future_x = self.__pos_x + 1
            elif self.__next_move == 'left':
                self.__direction = 'w'
                self.__future_x = self.__pos_x - 1
            else:
                self.__future_y = self.__pos_y - 1
        elif self.__direction == 's':
            if self.__next_move == 'right':
                self.__direction = 'w'
                self.__future_x = self.__pos_x - 1
            elif self.__next_move == 'left':
                self.__direction = 'e'
                self.__future_x = self.__pos_x + 1
            else:
                self.__future_y = self.__pos_y + 1
        elif self.__direction == 'e':
            if self.__next_move == 'right':
                self.__direction = 's'
                self.__future_y = self.__pos_y + 1
            elif self.__next_move == 'left':
                self.__direction = 'n'
                self.__future_y = self.__pos_y - 1
            else:
                self.__future_x = self.__pos_x + 1  
        else: 
            if self.__next_move == 'right':
                self.__direction = 'n'
                self.__future_y = self.__pos_y - 1
            elif self.__next_move == 'left':
                self.__direction = 's'
                self.__future_y = self.__pos_y + 1
            else:
                self.__future_x = self.__pos_x - 1

        return self.__future_x , self.__future_y

    def crashed(self): #sets crashed to True which is bad luck for this car :/
        self.__crashed = True
    def get_crashed(self):
        return self.__crashed

def referee_light_cycle(red_car,blue_car):
    global grid
    global grid_length

    red_current_x, red_current_y = red_car.state_transaction(grid,blue_car.get_car_state_string()) #Sends state information to red car and returns red cars current position
    red_desired_move_x, red_desired_move_y = red_car.update_position()                       #Translates where the red car wants to go and returns its desired_x and desired_y
    blue_current_x, blue_current_y = blue_car.state_transaction(grid,red_car.get_car_state_string())     #Sends state information to blue car and returns red cars current position
    blue_desired_move_x, blue_desired_move_y = blue_car.update_position()                    #Translates where the blue car wants to go and returns its desired_x and desired_y

    if red_desired_move_x == blue_desired_move_x and red_desired_move_y == blue_desired_move_y:
        print("Tie")
        sys.exit(0)

    #print('red_future_x: ',red_desired_move_x,'red_future_y: ',red_desired_move_y)
    #print('blue_future_x: ',blue_desired_move_x,'blue_future_y: ',blue_desired_move_y)

    if red_desired_move_x < 0 or red_desired_move_x > (grid_length - 1) or red_desired_move_y < 0 or red_desired_move_y > (grid_length - 1): #checks if red car wants to go off map if so that car has crashed
        red_car.crashed()


    if blue_desired_move_x < 0 or blue_desired_move_x > grid_length - 1 or blue_desired_move_y < 0 or blue_desired_move_y > grid_length - 1: #checks if blue car wants to go off map if so that car has crashed
        blue_car.crashed()

    if not red_car.get_crashed(): #checks if red car wants to move to an open space if not it has crashed   
        object_at_red_desired_position = grid[red_desired_move_y][red_desired_move_x]
        if object_at_red_desired_position != '.':
            red_car.crashed()
    if not blue_car.get_crashed(): #checks if blue car wants to move to an open space if not it has crashed 
        object_at_blue_desired_position = grid[blue_desired_move_y][blue_desired_move_x]
        if object_at_blue_desired_position != '.':
            blue_car.crashed()

    if red_car.get_crashed() and blue_car.get_crashed():
        print('Tie')
        sys.exit(0)
    elif red_car.get_crashed():
        print('Winner',blue_player_file)
        sys.exit(0)
    elif blue_car.get_crashed():
        print('Winner',red_player_file)
        sys.exit(0)
    else:
        grid[red_desired_move_y][red_desired_move_x] = 'R'
        grid[blue_desired_move_y][blue_desired_move_x] = 'B'
        grid[red_current_y][red_current_x] = 'W'
        grid[blue_current_y][blue_current_x] = 'W'

        red_car.change_pos()
        blue_car.change_pos()




def init_cars(time_out = 5):
    global grid
    global grid_length
    coin_flip = random.randint(0,1)

    if os.name == 'nt':
        red = pexpect.popen_spawn.PopenSpawn('python3 ' + red_player_file)
        blue = pexpect.popen_spawn.PopenSpawn('python3 ' + blue_player_file)
    else:
        # red = pexpect.spawn('python3 ' + red_player_file)  #spawn red player process
        # blue = pexpect.spawn('python3 ' + blue_player_file)#spawn blue player process
        red = pexpect.spawn('./' + red_player_file)  #spawn red player process
        blue = pexpect.spawn('./' + blue_player_file)#spawn blue player process

    #red.logfile_read = sys.stdout.buffer #tells pexpect to write all output to main process stdout should only be uncommited for debuging
    #blue.logfile = sys.stdout.buffer #tells pexpect to write all output to main process stdout should only be uncommited for debuging

    i = red.expect(['ready',pexpect.TIMEOUT,pexpect.EOF],timeout = time_out) #wait for red child process to send 'ready' 

    if i == 1:  #reacts on if red expect times out or errors        
        print('Time out on ' + red_player_file +'. Ready signal not sent in start transaction')
        sys.exit(0)
    elif i == 2:
        print('Program ended in file ' + red_player_file + ' : Program needs to not end on its own. Try useing an infinite loop and make sure your client doesnt crash')
        sys.exit(0)

    red.sendline(str(grid_length)) #sends grid_lenth to red process so it can build its model

    i = blue.expect(['ready',pexpect.TIMEOUT,pexpect.EOF],timeout = time_out) #wait for blue child process to send 'ready' 

    if i == 1:  #reacts on if blue expect times out or errors       
        print('Time out on ' + blue_player_file +'. Ready signal not sent in start transaction')
        sys.exit(0)
    elif i == 2:
        print('Program ended in file ' + blue_player_file + ' : Program needs to not end on its own. Try useing an infinite loop and make sure your client doesnt crash')
        sys.exit(0)

    blue.sendline(str(grid_length)) #sends grid_lenth to blue process so it can build its model



    if coin_flip == 0: #starts cars on random corner based of coin_flip value
        red_car = Bike(0,0,'s',red,red_player_file)
        blue_car = Bike(grid_length -1 ,grid_length - 1,'n',blue,blue_player_file)
        grid[0][0] = 'R'
        grid[grid_length - 1][grid_length - 1] = 'B'
    else:
        blue_car = Bike(0,0,'s',blue,blue_player_file)
        red_car = Bike(grid_length -1 ,grid_length - 1,'n',red,red_player_file)
        grid[0][0] = 'B'
        grid[grid_length - 1][grid_length - 1] = 'R'
    return red_car, blue_car



red_car, blue_car = init_cars() #initializes red and blue cars position and sends them information on grid size 
while True: 
    referee_light_cycle(red_car,blue_car)
    #os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(.1)
    pprint.pprint(grid)
    print()
