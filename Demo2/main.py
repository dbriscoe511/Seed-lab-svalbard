import time
import comms
import sys
import computer_vision as cv
import subprocess

system = comms.comm() # initialize i2c and display

''' 
This scrip initializes a prompt of what excersize to select, followed
Currently, the movement part of this excersize does not 
involve communication between processors.

'''

SLOW = 5
NORMAL = 10
FAST = 30
#These values are hard coded into the arduino on demo1, no need for this function for the first demo. 

def test_nocv():
    time.sleep(1)
    system.update_lcd("cal")
    system.power_on()
    send('No line detected')
    time.sleep(3)
    send(10)
    time.sleep(1)
    send(-2)
    time.sleep(1)
    send(0)
    time.sleep(3)
    send('stop')
    time.sleep(1)
    #send('turn')




state = 0
def send(angle):
    global state
    print(angle)
    print(state)
    
    if (not angle == 'No line detected' and not angle == 'turn' and not angle == 'stop'):
        state = 1 #do not revert to 0, that is only finding the tape.
        system.update_lcd("tracking")
    elif (angle == 'turn'):
        state = 2
        system.update_lcd("turning 90")
    elif (angle == 'stop'):
        system.update_lcd("stopping")
        state = 3
        system.r_vel(127)
        system.l_vel(127)
        time.sleep(0.5)
        system.shutdown_motors()
        system.update_lcd("powering down")

    prop = 0.05   
    if state == 1:
        angle = float(angle)
        system.r_vel(FAST+int(angle*prop)+127)
        system.l_vel(FAST-int(angle*prop)+127)
    elif state == 0:
        system.r_vel(FAST+127)
        system.l_vel(127-FAST)
        system.update_lcd("finding")
    if state == 2:
        system.angle(90)


def excersize1():
    cmd = [sys.executable, "-c", "import computer_vision as cv; gains = cv.camera_setup(); cv.cv_main(gains)"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    state = 0
    system.power_on()
    while process.poll() is None:
        angle = process.stdout.readline()
        angle = angle.decode('utf-8')
        angle = angle.strip('\n')
        print(angle)
        send(angle)


        #time.sleep(0.5)
        #system.update_lcd(str(angle))

exr = int(input("what excersize?\n1: test no cv\n2: test cv\n"))
if exr ==1:
    #angle(degree), dist
    test_nocv()
else:
    excersize1()


