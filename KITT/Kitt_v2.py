from machine import Pin, PWM

class Led:
    pwm = None
    brightness = 0
    status = 0
    max_ticks_on=50
    ticks_on = 0
    max_brightness = 16000
    def __init__(self, gpio_pos, gpio_gnd):
        gnd_pin = Pin(gpio_gnd, Pin.OUT)
        gnd_pin.low()
        self.pwm = PWM(Pin(gpio_pos))
        self.pwm.freq(1024)
        self.pwm.duty_u16(0)
       
    def set_brightness(self, level_u16):
        if level_u16 < 0:
            level_u16 = 0
        self.pwm.duty_u16(level_u16)
        self.brightness = level_u16
   
    def get_brightness(self):
        return self.brightness
   
    def isPoweringOn(self):
        return self.status == 1
   
    def isPowerOn(self):
        return self.status == 2

    def isPoweringOff(self):
        return self.status == 3
   
    def powerOn(self):
        self.status = 1
       
       
leds=dict()

leds[0] = Led(17, 14)
leds[1] = Led(18, 13)
leds[2] = Led(19, 12)
leds[3] = Led(20, 11)
leds[4] = Led(21, 10)
leds[5] = Led(22, 9)
leds[0].powerOn()

direction=0
active_led=0

def get_nextLed():
    global direction, active_led
    if direction == 0:
        if active_led < 5:
            active_led += 1
        else:
            active_led = 4
            direction = 1
    else:
        if active_led > 0:
            active_led -= 1
        else:
            active_led = 1
            direction = 0
    return leds[active_led]
   
while (1):
    for led in range(6):
        if leds[led].isPoweringOn():
            if leds[led].get_brightness() < leds[led].max_brightness:
                leds[led].set_brightness(leds[led].get_brightness() + 70)
            else:
                leds[led].status = 2    
                leds[led].ticks_on = 0
        elif leds[led].isPowerOn():
            if leds[led].ticks_on < leds[led].max_ticks_on:
                leds[led].ticks_on+=1
            else:
                leds[led].status = 3
                get_nextLed().powerOn()
        elif leds[led].isPoweringOff():
            if leds[led].get_brightness() > 0:
                leds[led].set_brightness(leds[led].get_brightness() - 70)
            else:
                leds[led].status = 0
