#!/usr/bin/env python3

from mazes import *
from time import sleep
SLEEP_TIME=0.15
SYSTEM_CLEAR=False
from math import cos, sin, pi, atan2

class Ultrasonics:
    def __init__(self, maze):
        self.ultra1=None
        self.ultra2=None
        self.ultra3=None          
        self.maze=maze    
        self.gap=self.initial_position("R") 
        self.arrows_dict={0:'→', pi/2:'↑',pi:'←', 3*pi/2:'↓'}

        
    def start_route(self):
        self.maze[self.gap[1]+1][self.gap[0]]=' '
        self.maze[self.gap[1]][self.gap[0]]=self.arrows_dict[pi/2]
        self.real_path()
        
    def print_route(self, previous_pos, current_pos, direction):
        self.maze[-previous_pos[1]+self.gap[1]][previous_pos[0]+self.gap[0]]=' '
        self.maze[-current_pos[1]+self.gap[1]][current_pos[0]+self.gap[0]]=self.arrows_dict[direction]
        self.real_path()
        print("")            
        
    def initial_position(self, letter):
        for i in self.maze[-1]:
            if letter in i:
                #print(self.maze[-1].index(i),len(self.maze)-2)
                sleep(SLEEP_TIME)
                return (self.maze[-1].index(i),len(self.maze)-2)
            else:
                continue

    def real_path(self):
        for i in self.maze:
            for j in i:
                print(j + ' ', end="")
            print("")        
        
    def get_observations(self, position,direction):
        self.actual_x, self.actual_y=position[0]+self.gap[0],-position[1]+self.gap[1]
        # left, up, right
        positions=[(direction+pi/2)%(2*pi),direction, (direction-pi/2)%(2*pi)]
        moves=[]
        for pos in positions:
            moves.append(list(map(lambda x:x(pos), (cos, sin))))
        for move in moves:
            move[0]=0 if abs(move[0])<0.1 else int(move[0])
            move[1]=0 if abs(move[1])<0.1 else int(move[1])
        observations=()
        for move in moves:
                neighbour=(position[0]+move[0], position[1]+move[1])
                neighbour_real=(self.actual_x+move[0], self.actual_y-move[1])
                if self.maze[neighbour_real[1]][neighbour_real[0]]=='#':
                    observations=observations+(0,)             
                elif self.maze[neighbour_real[1]][neighbour_real[0]]==' ':
                    observations=observations+(1,)
                elif self.maze[neighbour_real[1]][neighbour_real[0]]=='X':
                    observations=observations+(2,)
        return observations

