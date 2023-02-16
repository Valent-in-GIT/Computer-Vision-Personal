from machine import Pin
import utime


class Ultrasonics:
    def __init__(self):
        self.trigger_f=Pin(8, Pin.OUT)
        self.echo_f = Pin(9, Pin.IN)
        
        self.trigger_l = Pin(12, Pin.OUT)
        self.echo_l = Pin(13, Pin.IN)

        self.trigger_r = Pin(4, Pin.OUT)
        self.echo_r = Pin(5, Pin.IN)
        
    def get_lecture(self):
        front = self.ultra(self.trigger_f, self.echo_f)
        utime.sleep_ms(100)
        left = self.ultra(self.trigger_l,self.echo_l)
        utime.sleep_ms(100)
        right = self.ultra(self.trigger_r,self.echo_r)        
        utime.sleep_ms(100)
        sonar = [left, front, right]
        return sonar
    
    def measure_front(self):
        self.trigger_f.low()
        utime.sleep_us(2)
        self.trigger_f.high()
        utime.sleep_us(5)
        self.trigger_f.low()
        while self.echo_f.value() == 0:
            signaloff = utime.ticks_us()
        while self.echo_f.value() == 1:
            signalon = utime.ticks_us()
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        return distance


    def ultra(self,trigger,echo):
        trigger.low()
        utime.sleep_us(2)
        trigger.high()
        utime.sleep_us(5)
        trigger.low()
        while echo.value() == 0:
            signaloff = utime.ticks_us()
        while echo.value() == 1:
            signalon = utime.ticks_us()
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        return_value= 1 if (distance<15) else 0
        #return_value = 2 if (distance>120) else return_value
        return return_value



def main():
    ultra=Ultrasonics()
    
    ultra.get_lecture()
        
if __name__ == '__main__':
    main()