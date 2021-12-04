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
FAST = 40
#These values are hard coded into the arduino on demo1, no need for this function for the first demo. 
state = 0
stopTest = 0
startWait = 0
pastAngle = 0
def test_nocv():
    global state
    while(True):
        state = 0
        time.sleep(1)
        system.update_lcd("cal")
        system.power_on()
        send('No line detected')
        time.sleep(3)
        send(10)
        time.sleep(5)
        send(-2)
        time.sleep(0.5)
        send(0)
        time.sleep(0)
        send('stop')
        time.sleep(1)
        #send('turn')




def send(angle):
    global state
    global stopTest
    global pastAngle
    global startWait
    if startWait == 0:
        time.sleep(1)
        startWait = 1
    prop = 0.4 
    print(angle)
    print(state)
    
    if (not angle == 'No line detected' and not angle == 'turn' and not angle == 'stop' and not angle == ''):
        #while( abs(float(angle)) > 6):
        #    time.sleep(0.1)
        state = 1 #do not revert to 0, that is only finding the tape.
        system.update_lcd("tracking")
        
    elif (angle == 'turn'):
        state = 2
        system.update_lcd("turning 90")
    elif angle == 'stop' or stopTest >= 15: #If the robot sees no line after seeing a line, or 'stop' is sent
        system.update_lcd("stopping")
        state = 3
        if stopTest < 15:
            time.sleep(1.2)
        #stop the motors
        system.r_vel(127)
        system.l_vel(127)
        system.shutdown_motors()
        system.update_lcd("powering down")
        exit(0)
    else:
        state = 0

    
    if state == 1:
        if (not angle == 'No line detected' and not angle == 'turn' and not angle == 'stop' and not angle == ''):
            angle = float(angle)
            print('state = 1 (track)')
            #Rotate the robot's center to match the tape center
            stopTest = 0
            system.r_vel(20-int(angle*prop)+127)
            system.l_vel(20+int(angle*prop)+127)
            pastAngle = angle
    elif state == 0:
        #Rotate until it finds tape
        
        print('state = 0 (find)')
        system.update_lcd("finding")
        if pastAngle < 0:
            sign = -1
        else:
            sign = 1
            
        stopTest += 1

        system.r_vel(127-sign*12)
        system.l_vel(127+sign*12)
        #(0.1)
        
    if state == 2:
        system.angle(90)


def excersize1():
    system.shutdown_motors()
    system.r_vel(127)
    system.l_vel(127)
    
    #cmd runs computer_vision.py as a subprocess. Angle is extracted from output
    cmd = [sys.executable, "-c", "import computer_vision as cv; gains = cv.camera_setup(); cv.cv_main(gains)"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    global state
    global startWait
    state = 0
    
    
    while process.poll() is None:
        system.power_on()
        
        angle = process.stdout.readline()
        angle = angle.decode('utf-8')
        angle = angle.strip('\n')
        #print(angle)
        send(angle)
        
        
    system.r_vel(127)
    system.l_vel(127)
    system.shutdown_motors()
    exit(0)
        #time.sleep(0.5)
        #system.update_lcd(str(angle))

exr = int(input("what excersize?\n1: test no cv\n2: test cv\n"))
if exr ==1:
    #angle(degree), dist
    test_nocv()
else:
    excersize1()


