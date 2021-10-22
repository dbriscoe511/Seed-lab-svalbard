import time
import comms
import sys

system = comms.comm() # initialize i2c and display

#These values are hard coded into the arduino on demo1, no need for this function for the first demo. 
def excersize2(angle,dist):
    time.sleep(8)
    system.angle(angle)
    
    system.move(dist*12)

def excersize1():
    while (True):
        time.sleep(0.1)
        t_angle = sys.stdin.readline()
        system.update_lcd(str(t_angle))

exr = int(input("what excersize? (1: camera angle test, 2 (obsolete): rotate/drive test)"))
if exr ==2:
    #angle(degree), dist
    excersize2(90,5)
else:
    excersize1()

