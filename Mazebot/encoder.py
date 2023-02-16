import machine
import utime

#función de interrupción
def encoder_handler(pin):
    global paso
    paso += 1


def main():
    global paso
    paso = 0
    frequency = 10000 #10KHz
    r_pwm = machine.PWM(machine.Pin(18)) #PWM derecha
    r_pwm.freq(frequency)
    l_pwm = machine.PWM(machine.Pin(19)) #PWM izquierda
    l_pwm.freq(frequency)

    encoder = machine.Pin(0, machine.Pin.IN)
    encoder.irq(trigger=machine.Pin.IRQ_FALLING, handler=encoder_handler)
    
    timer_start = utime.ticks_ms()
    
    while True:
        velocidad = 65536;
        r_pwm.duty_u16(velocidad)
        l_pwm.duty_u16(0)
        
        timer_elapsed = utime.ticks_diff(utime.ticks_ms(), timer_start)
        if timer_elapsed >= 1000:
            #Calculo de las RPM (20 aspas)
            state = machine.disable_irq()
            rpm = paso*60/960
            paso = 0
            machine.enable_irq(state)
            timer_start = utime.ticks_ms()
            print(rpm, 'RPM')
            
if __name__ == '__main__':
    main()