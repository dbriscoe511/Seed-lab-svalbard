
'''
Handles i2c and lcd interfacing. 

this is called by main when data needs to be sent or recived 
to use, create a comm object, and call it's functions

The command function and it's derivatives are not used in demo 1
and can be ignored. 

'''
import smbus2 
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as chlcd
import time

SLOW = 20
NORMAL = 80
FAST = 150

LEFT_WHEEL_VEL = 0
RIGHT_WHEEL_VEL = 1
DIST = 2
ANGLE = 3
SHUTDOWN = 4
POWERON = 5

class comm:
        bus = 0
        addr = 0
        lcd = 0
        lcd_i2c= 0

        def __init__(self):
                self.bus = smbus2.SMBus(1) # initializes an i2c line with smbus protocol
                self.addr = 4 # i2c address of slave device. needs to match in arduino code
                time.sleep(0.2)

                self.lcd_i2c = board.I2C() # the LCD is not smbus complient, so a seperate i2c line is initialized on the same line 
                self.lcd = chlcd.Character_LCD_RGB_I2C(self.lcd_i2c,16,2) # config code specific to this lcd
                self.lcd.message = "initialized"
                time.sleep(0.2)

        def command(self,command,val):
            # not used for this demo. 
            #sends a mutually agreed upon command between the pi and the arduino,
            #follwed by a velocity amount
            if val<0 or val>255:
                        raise ValueError("outside of byte range") # must be a byte
            if command<0 or command>6:
                        raise ValueError("command does not exist") # must be a byte
            print(self.addr)
            print([command,val])
            self.bus.write_i2c_block_data(self.addr,0,[command,val])
            time.sleep(0.1)

        def move(self,distance): # in 1in incrments
            self.command(DIST,distance)
        
        def angle(self,angle):
            a = angle/4
            self.command(ANGLE,a)
            
        def shutdown_motors(self):
            self.command(SHUTDOWN,0)
        def power_on(self):
            self.command(POWERON,0)
        def r_vel(self,vel):
            self.command(RIGHT_WHEEL_VEL,vel)

        def l_vel(self,vel):
            self.command(LEFT_WHEEL_VEL,vel)

        def vel(self,vel):
            self.command(LEFT_WHEEL_VEL,vel)
            self.command(RIGHT_WHEEL_VEL,vel)

        def stop(self):
            self.command(LEFT_WHEEL_VEL,0)
            self.command(RIGHT_WHEEL_VEL,0)


        def read(self):
                return self.bus.read_block(self.addr)
        def update_lcd(self,val):
                self.lcd.clear()
                self.lcd.message = str(val)
        
