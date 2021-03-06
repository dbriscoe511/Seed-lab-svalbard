
'''
Handles i2c and lcd interfacing. 

this is called by main when data needs to be sent or recived 
to use, create a comm object, and call it's functions

'''
import smbus2 
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as chlcd
import time

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

        def send(self,val):
                if val<0 or val>255:
                        raise ValueError("outside of byte range") # must be a byte
                self.bus.write_byte(self.addr,val)
        def read(self):
                return self.bus.read_byte(self.addr)
        def update_lcd(self,val):
                self.lcd.clear()
                self.lcd.message = str(val)
        
                