import time
import comms
import sys

system = comms.comm() # initialize i2c and display

def excersize2(angle,dist):
    time.sleep(8)
    system.angle(angle)
    
    system.move(dist*12)

def excersize1():
    while (True):
        time.sleep(0.1)
        t_angle = sys.stdin.readline()
        system.update_lcd(str(t_angle))

excersize2(90,5)
excersize1()


