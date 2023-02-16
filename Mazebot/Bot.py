from machine import PWM, Pin, I2C, ADC
from utime import sleep_ms
from ssd1306 import SSD1306_I2C
import framebuf
from ultrasonics import *

PROPORCION=0.8
VELOCITY_R=int((0.805)*65536)
VELOCITY_L=int((0.75)*65536)
frequency=(10000)
WIDTH = 128
HEIGHT = 64


class Bot:
    def __init__(self, Ultra):
        self.l1 = PWM(Pin(18))
        self.l1.freq(frequency)
        self.l2 = PWM(Pin(19))
        self.l2.freq(frequency)
        self.step1=0
        self.step2=0
        
        self.Ultra=Ultra
        
        
        self.r1 = PWM(Pin(20))
        self.r1.freq(frequency)
        self.r2 = PWM(Pin(21))
        self.r2.freq(frequency)
        self.stop()
        
        #self.i2c= I2C(1, scl = Pin(15), sda= Pin(14), freq = 200000)    
        #self.oled = SSD1306_I2C(WIDTH, HEIGHT, self.i2c)
        #self.erase_oled()
        
        self.encoder2 = Pin(0, Pin.IN)
        self.encoder2.irq(trigger=Pin.IRQ_RISING, handler=self.en2_handler)
        
        self.encoder1 = Pin(2, Pin.IN)
        self.encoder1.irq(trigger=Pin.IRQ_RISING, handler=self.en1_handler)
        
    def en2_handler(self,Pin):
        self.det1=True
        self.step1 += 1
        print(self.step1)
    
    def en1_handler(self,Pin):
        self.det2=True
        self.step2 += 1
        print(self.step2)
    
        
    def left_direction(self):
        self.l1.duty_u16(0)
        self.l2.duty_u16(VELOCITY_L)
        self.r1.duty_u16(VELOCITY_R)
        self.r2.duty_u16(0)
        #sleep_ms(410)
        self.det2=False
        self.step2=0
        while self.step2 < 55:
            if self.det2:
                self.det2=False

    def right_direction(self):
        self.l1.duty_u16(VELOCITY_L)
        self.l2.duty_u16(0)
        self.r1.duty_u16(0)
        self.r2.duty_u16(VELOCITY_R)
        #sleep_ms(410)
        self.det1=False
        self.step1=0
        while self.step1 < 58:
            if self.det1:
                self.det1=False

    def front_direction(self):
        self.l1.duty_u16(VELOCITY_L)
        self.l2.duty_u16(0)
        self.r1.duty_u16(VELOCITY_R)
        self.r2.duty_u16(0)
        self.det1=False
        self.step1=0
        while self.step1 < 20:
            front=self.Ultra.measure_front()
            if  front< 5:
                print(front)
                self.stop()
                break
            if self.det1:
                self.det1=False
        
    def stop(self):
        self.l1.duty_u16(0)
        self.l2.duty_u16(0)
        self.r1.duty_u16(0)
        self.r2.duty_u16(0)
        sleep_ms(500)
        
    def run(self):
        self.front_direction()
        self.left_direction()
        self.right_direction()
        self.stop()
    
    def listener(self, turns):
        negative = True if turns < 0 else False
        while turns != 0:
            turns = turns - 1 if turns > 0 else turns + 1
            if negative:
                #self.print_oled("DERECHA")
                self.right_direction()
                self.stop()
                #self.erase_oled()
                self.stop()
                sleep_ms(500)                
                
            else:
                #self.print_oled("IZQUIERDA")
                self.left_direction()
                self.stop()
                #self.erase_oled()
                sleep_ms(500)   
        #self.print_oled("AVANZA")
        #self.front_direction()
        #self.stop()
        #self.erase_oled()
        sleep_ms(500)
    
    #def print_oled(self, text):
    #    self.oled.text(str(text), 0, 0)        
    #    self.oled.show()

        
    #def erase_oled(self):
    #    self.oled.fill(0)
        

def main():
    bot=Bot(Ultrasonics())
    bot.front_direction()
    bot.stop()
    
if __name__ == '__main__':
    main()