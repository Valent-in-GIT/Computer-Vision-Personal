#!/usr/bin/env python3

from math import cos, sin, pi, atan2
from utime import sleep_ms
SLEEP_TIME=150

class DFS:
    def __init__(self, Ultrasonics=None, Bot=None):
        self.Ultrasonics=Ultrasonics
        self.Bot=Bot
        self.visited = ()
        self.pending = ()
        self.node_objs = ()
        self.current_pos=(0,0)
        self.previous_pos=self.current_pos
        self.observations_dict={0:(-1,0),1:(0,1),2:(1,0)}
        self.actual_obj = None
        self.returning=False        
        self.first_return=True     
        self.dir=pi/2    
        
    def dfs(self):
        """
        Create the trajectory based on a DFS algorithm (go to deepest position).
        """
        print("hey")
        self.returning=False
        try:
            self.pending[-1] in self.visited
        except:
            return
        if self.pending[-1] in self.visited:
        
            self.previous_pos=self.current_pos
            return
        else:
            self.previous_pos=self.current_pos
            self.goal_position=self.pending[-1]
            self.pending=self.pending[:-1]
            self.goal_obj=self.node_objs[-1]
            self.goal_origin=self.goal_obj.origin                    
        
        
            if self.goal_obj.origin==None:
                pass
            else:
                while tuple(self.actual_obj.position)!=tuple(self.goal_obj.origin.position):
                    self.returning=True
                    self.return_to_higher()
            if self.returning:
                self.previous_pos=self.current_pos
                self.previous_dir=self.dir
                self.dir=self.get_direction(self.goal_obj.origin.position)
                self.current_pos =self.goal_obj.origin.position
                self.actual_obj=self.node_objs[-1]
                self.node_objs=self.node_objs[:-1]
                self.publisher()
                #self.Ultrasonics.print_route(self.previous_pos, self.current_pos, self.dir)
                sleep_ms(SLEEP_TIME)
                return
            self.first_return=True
            self.current_pos =self.goal_position
            self.actual_obj = self.node_objs[-1]
            self.node_objs=self.node_objs[:-1]
            self.previous_dir=self.dir
            self.dir=self.actual_obj.direction
            self.publisher()
            self.Bot.print_oled(str(self.current_pos)+str(self.previous_dir))
            sleep_ms(500)
            self.Bot.erase_oled()
            #self.Ultrasonics.print_route(self.previous_pos, self.current_pos, self.dir)
            sleep_ms(SLEEP_TIME)

    def return_to_higher(self):
        """
        Occurs when the current position its different of the next node (when there are no more available paths on the current node), returning to the next farthest node from begin. 
        """
        if self.first_return:
            self.first_return=False
            neighbour=self.actual_obj.origin.position
            self.previous_dir=self.dir
            self.dir=self.get_direction(neighbour)
            self.previous_pos=self.current_pos
            self.current_pos=self.actual_obj.position
            self.publisher()
            #self.Ultrasonics.print_route(self.previous_pos, self.current_pos, self.dir)
            sleep_ms(SLEEP_TIME)
            self.actual_obj=self.actual_obj.origin        
            return    
        neighbour=self.actual_obj.position
        self.previous_dir=self.dir
        self.dir=self.get_direction(neighbour)
        self.previous_pos=self.current_pos
        self.current_pos=self.actual_obj.position
        if self.previous_pos == self.current_pos:
            self.actual_obj=self.actual_obj.origin
            return
        self.actual_obj=self.actual_obj.origin
        self.publisher()
        #self.Ultrasonics.print_route(self.previous_pos, self.current_pos, self.dir)
        sleep_ms(SLEEP_TIME)           
            
    def publisher(self):
        """
        Publish the movement commands for the Robotm, publishes the number of turns to reach next direction, negative integer indicates counterclockwise direction.
        """ 
        turns=int(atan2(sin(self.dir-self.previous_dir), cos(self.dir-self.previous_dir))/(pi/2))
        print(turns)
        self.Bot.listener(turns)
           
    def get_direction(self, neighbour):
        """
        Returns the direction of the current position based on its origin.
        """
        print(f" get direction, neighbour is {neighbour} current pos is {self.current_pos}")
        if tuple(neighbour) == self.current_pos:
            return self.dir
        direction=atan2(neighbour[1]-self.current_pos[1],neighbour[0]-self.current_pos[0])
        direction=direction%(2*pi)
        return direction    


    def run(self):
        """
        Appends the new paths based on the observation of the ultrasonic sensors. If all of them cant measure any wall, assumes goal is reached. This function uses an infinite while loop until goal is reached.
        """
        print("from run dfs")
        #self.Ultrasonics.real_path()
        #sleep_ms(SLEEP_TIME)
        #self.Ultrasonics.start_route()
        #sleep_ms(SLEEP_TIME)
        while True:
            # Append to visited the current position
            self.visited=self.visited + (self.current_pos,)
            # Set an empty tuple of neighbours to append new ones. 
            self.neighbours=()
            # Get ultrasonics observations
            print("Before observations")
            observations=self.Ultrasonics.get_lecture()
            print("After observations")
            self.Bot.print_oled(observations)
            self.Bot.erase_oled()
            sleep_ms(1500)
            print(observations)
            if (observations[0]+observations[1]+observations[2])>5:
                return
            
            moves=[]
            positions=[(self.dir+pi/2)%(2*pi),self.dir, (self.dir-pi/2)%(2*pi)]
            for i in range(len(positions)):
                if observations[i]==0 or observations[i]==2:
                    moves.append(list(map(lambda x:x(positions[i]), (cos, sin))))
                    
            for move in moves:
                move[0]=0 if abs(move[0])<0.1 else int(move[0])
                move[1]=0 if abs(move[1])<0.1 else int(move[1])
                
                neighbour=(self.current_pos[0]+move[0], self.current_pos[1]+move[1])
                if neighbour in self.visited:
                    continue
                else:
                    self.move=Tree((neighbour[0], neighbour[1]))
                    self.pending= self.pending+(neighbour,)
                    self.node_objs=self.node_objs+(self.move,)
                    direction=self.get_direction(neighbour)
                    self.move.add_origin(self.actual_obj, direction)
            
            # Adds to current position if there is an observation, observations dicts stores the values of the observation (left, up, right)
            print(f"pending are {self.pending}")
            self.dfs()

class Tree:
    def __init__(self, position):
        self.origin=None
        self.position=position
        self.direction=None

    def add_origin(self, father_position, direction):
        self.origin=father_position
        self.direction=direction

def main():
    pass

if __name__ == '__main__':
    main()