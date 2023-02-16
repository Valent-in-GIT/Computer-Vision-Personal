#!/usr/bin/env python3

from dfs_algorithm import *
from mazes import *
from ultrasonics import *
from Bot import *
from machine import Pin
from  utime import sleep_ms

import _thread
import sys

MAZE_NUM=5
        
class Execute:
    def __init__(self):
        self.maze_dict={1:Maze1,2:Maze2,3:Maze3, 4:Maze4, 5:Maze5}
        self.led=Pin(27, Pin.OUT)
        self.led.off()
        self.push_b=Pin(26, Pin.IN)
        self.Ultrasonics=Ultrasonics()
        #self.Ultrasonics=Ultrasonics(self.maze_dict[MAZE_NUM])
        self.Bot=Bot(self.Ultrasonics)
        self.Bot.erase_oled()
        
        

    def execute(self):
        DFS(self.Ultrasonics,self.Bot).run()
    
    def blink(self):
        for i in range(11):
            self.led.value(i%2)
            sleep_ms(50)

"""
    x=""
    def Lectura():
        while True:
            global x
            data=str(sys.stdin.readline())
            x=data
            sleep_ms(1000)
    _thread.start_new_thread(Lectura, ())
"""

def main():
        execute=Execute()
        while True:
            if execute.push_b.value():
                break
        execute.blink()
        execute.execute()
        execute.Bot.erase_oled()
        #sys.stdout.write(sonar+"\r\n")
        
        
if __name__=='__main__':
    main()