
import machine
from Bot import *
from math import pi
from utime import ticks_diff,ticks_us
det1=det2=False
step1=step2=0

def en1_handler(Pin):
    global step1, det1
    det1=True
    step1 += 1
    
def en2_handler(Pin):
    global step2, det2
    det2=True
    step2 += 1
    

encoder1 = machine.Pin(2, machine.Pin.IN)
encoder1.irq(trigger=machine.Pin.IRQ_FALLING, handler=en1_handler)

encoder2 = machine.Pin(0, machine.Pin.IN)
encoder2.irq(trigger=machine.Pin.IRQ_FALLING, handler=en2_handler)

def main():
    bot=Bot()
    bot.front_direction()
    global det1, det2, step1, step2
    timer_start1 = ticks_us()
    timer_start2 = ticks_us()
    while True:
        if det1 and (step1%2==1):      
            timer_elapsed1 = ticks_diff(ticks_us(),timer_start1)
            det1=False
            timer_elapsed1=1 if timer_elapsed1==0 else timer_elapsed1
            #print(f"left encoder angular velocity {(pi/5)*1000000*(1/48)/(timer_elapsed1)} rad/s")
            timer_start1 = ticks_us()
        
        elif det2 and (step2%2==0):
            print(f"right encoder, step is {step2}")
            timer_elapsed2 = ticks_diff(ticks_us(),timer_start2)            
            timer_elapsed2=1 if timer_elapsed2==0 else timer_elapsed2
            print(f"left encoder angular velocity {(pi/5)*1000000*(1/48)/(timer_elapsed2)} rad/s")
            det2=False
            timer_start2 = ticks_us()

if __name__ == '__main__':
    main()
        