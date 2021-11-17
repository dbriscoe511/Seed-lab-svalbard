import time
import comms
import sys
import computer_vision as cv
import subprocess

system = comms.comm() # initialize i2c and display

''' 
This scrip initializes a prompt of what test to select, the camera script is ccalled with a subprocess,
and the angle that is returned from computer vision times a proportional constant is fed to as a difference in speed between the two wheels.
CV takes care of identifying diffirent robot states, such as stop/move/find 


the send function keeps track of the robot state and calls the comms functions, 
test_nocv inputs a set of velocity commands to test the robot movement. 
run_with_cv opens the subprocess and starts the script

This main loop should be run with MAIN.ino on the arduino 


'''
# these variables are preset speeds, to abstract code 
SLOW = 7
NORMAL = 10 
FAST = 40


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
        system.power_on() # enable motors 
        send('No line detected') # put the robot in find state (slow spin) 
        time.sleep(3)
        send(10) # do a sweeping left turn
        time.sleep(5)
        send(-2) #slight right turn
        time.sleep(0.5)
        send(0) #forward
        time.sleep(0)
        send('stop') #stop
        time.sleep(1)
        




def send(angle):
    global state
    global stopTest
    global pastAngle
    prop = 0.4 #angle multiplier for speed feed
    print(angle)
    print(state)
    
    if (not angle == 'No line detected' and not angle == 'turn' and not angle == 'stop' and not angle == ''):
        #while( abs(float(angle)) > 6):
        #    time.sleep(0.1)
        state = 1 #do not revert to 0, that is only finding the tape.
        system.update_lcd("tracking")
        
    elif (angle == 'turn'): # unused for demo 2, will be used for sharp corners in final project 
        state = 2
        system.update_lcd("turning 90")
    elif (angle == 'No line detected' and stopTest > 3) or angle == 'stop': #If the robot sees no line after seeing a line, or 'stop' is sent
        system.update_lcd("stopping")
        state = 3
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
            #Rorate the robot's center to match the tape center
            system.r_vel(35-int(angle*prop)+127)
            system.l_vel(35+int(angle*prop)+127)
            stopTest += 1
            pastAngle = angle
    elif state == 0:
        #Rotate until it finds tape
        if stopTest > 0:
            stopTest -= 1
        print('state = 0 (find)')
        system.update_lcd("finding")
        system.r_vel(SLOW+127)
        system.l_vel(127-SLOW)
        
    if state == 2: #unused for this demo
        system.angle(90)


def run_with_cv():
    system.shutdown_motors() # Make sure the robot is stopped
    system.r_vel(127)
    system.l_vel(127)
    

    cmd = [sys.executable, "-c", "import computer_vision as cv; gains = cv.camera_setup(); cv.cv_main(gains)"] # setup camera as a subprocess
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)# open camera as a subprocess
    global state
    global startWait
    state = 0
    
    
    while process.poll() is None: #while the camera is sending data
        if startWait == 0: # forces the robot to stay asleep until its ready
            time.sleep(0.3)
            system.power_on()
            startWait = 1
        angle = process.stdout.readline() # take in printed values from subprocess
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

exr = int(input("what excersize?\n1: test no cv\n2: test cv\n")) #excersize selection logic
if exr ==1:
    #angle(degree), dist
    test_nocv()
else:
    run_with_cv()


