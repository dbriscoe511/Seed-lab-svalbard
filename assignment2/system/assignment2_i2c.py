'''
This python file covers all excercises in assignment2
First flash the arduino with the excersize code you want to use (simply labeld as ex*.ino, with the * being the excersize number), then run this code.
The code will ask you what excersize to run and provide you with a set of instructions within the terminal 


'''



import smbus2 
import adafruit_character_lcd.character_lcd_rgb_i2c as chlcd
import time
import serial
import board

bus = smbus2.SMBus(1) # initializes an i2c line with smbus protocol
addr = 4 # i2c address of slave device. needs to match in arduino code

lcd_i2c = board.I2C() # the LCD is not smbus complient, so a seperate i2c line is initialized on the same line 
lcd = chlcd.Character_LCD_RGB_I2C(lcd_i2c,16,2) # config code specific to this lcd
#lcd.clear()


def basic_i2c():
    print('basic i2c test')
    send = int(input('enter a number'))
    bus.write_byte(addr,send) # uses the SMBus library to send data to the arduino over i2c

    time.sleep(.1) # give arduino time to process data

    n = bus.read_byte(addr)
    print(n)
    print('sent a '+str(send)+' recived a '+str(n))

def comm_link():
    print("comm link excersize")
    offset = int(input('enter a offset'))
    if offset <0 or offset>5:
        raise ValueError('offset out of range') # the arduino code can only handle 5 diffirent offset numbers
    send = int(input('enter a number'))
    bus.write_byte_data(addr, offset,send) # writes both the offset and the value

    time.sleep(1)
    offsetr = int(input('enter a offset to read'))
    bus.write_byte(addr,offsetr) # tells the arduino what will need to be read 
    recived = bus.read_byte(addr)
    print(recived)
    return [recived,offset,offsetr,send] #returns an array with arduino output, for use in other functions
    
def comm_link_led():
    print("comm link excersize with LCD")
    data = comm_link()  #simple calls the other version of this excersize and then displays the output on the LCD
    lcd.clear()
    lcd.message = "data recived: "+str(data[0])+"\ndatasent: " +str(data[3])

def string_communications():
    print("string communication excersize")
    send = input("enter a 32 char or less string")
    if len(send) == 0 or len(send)>30:
        raise ValueError('string out of range')

    rec = []
    send = [ord(s) for s in send]       # makes the message into bytes that can be sent over i2c
    try:                                # makes sure the program does not quit if there is a comm error
        bus.write_i2c_block_data(addr,0,send)
        time.sleep(3)
        rec = bus.read_i2c_block_data(addr,0,len(send))
    except:
        print("I2c error")
        lcd.clear()
        lcd.message = "I2c error"

    
    
    rec = [chr(r) for r in rec] # converts the i2c message into charecters using list comprehension
    empt = ""
    print(empt.join(rec)) #makes char array to string and prints

def read_pot():
    print("pot excersize")
    cycles = range(0,12)
    for i in cycles:  # reads the voltage a bunch of times, with delays imbetween to give tiome to test
        time.sleep(1.5)
        value = [bus.read_byte(addr),bus.read_byte(addr)] # the data is split into 2 bytes. the arduino takes care of deciding what byte needs to be sent 
        print(value)

        value = int.from_bytes(value,byteorder = 'big') #comibines two bytes and turns them into an integer
        value = round(float(value)*5/1024,2) #adc math to turn into a voltage
        print(value)
        lcd.clear()
        lcd.message = str(value)

def basic_serial():
    ser = serial.Serial('/dev/ttyACM0',115200)
    time.sleep(2) #make sure connection of peripherals is ready.
    print('basic serial test')
    send = bytes(input('enter a number'),'utf-8')

    ser.write(send)
    n=0
    time.sleep(1)

    while(ser.in_waiting>0): #waits until a serial message is ready. Note: the arduino serial console CANNOT be open
        try:
            n = ser.readline().decode('utf8').rstrip() #decodes from serial
            print(n)
            print("rec")
        except:
            print("communication error")

    print('sent a '+str(send)+'recived a '+str(n))

while True:
    ex = int(input("enter excersize number"))
    if ex == 1:
        basic_i2c()
    elif ex == 2:
        comm_link()
    elif ex == 3:
        comm_link_led()
    elif ex == 4:
        print("any excersize number on the arduino is ok for this test. ex1 reccommended.")
        print("use cntrl -c to exit")
        while True:
            time.sleep(1)
            bus.write(10,255)
    elif ex == 5:
        string_communications()
    elif ex == 6:
        read_pot()
    elif ex == 7:
        string_communications()
    elif ex == 8:
        basic_serial()
    else:
        print("invalid")


        


    




