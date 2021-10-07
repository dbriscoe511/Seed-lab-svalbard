'''
This code runs the miniproject. 

To use, flash the arduino with miniproj.ino, connect needed peripherals, and run. 

To exit the script hit ctnl-C


'''


import time
import comms
import miniproj_cv as mcv

previous_angle = 1

system = comms.comm() # initialize i2c and display

camera = mcv.setup_camera() #initialize cam
camera = mcv.calibrate(camera) #calibrate for lighting

while True:
    #check comp vision, get angle

    t_angle = mcv.capture_angle(camera)
    #print(str(t_angle)+'\n\n\n')
    if(t_angle>13.5): # these angles are based on the fov of the camera. this serializes the unkown angles to a number corresponding to a direction for the motor.
        angle = 4
    elif(t_angle>0):
        angle = 3
    elif(t_angle>-13.5):
        angle = 2
    else:
        angle = 1

    measured_angle = 0
    time.sleep(0.5)

    if not angle == previous_angle: # no need to resend the same thing
        print("sending...")
        if(angle-previous_angle>0): # this gives a realative angle to where the wheel is at. Unused, could be removed
            encoderangle = (angle-previous_angle)
        else:
            encoderangle = (angle-previous_angle+4)%4

        
        system.send(int(angle))

        time.sleep(0.5) # give the wheel time to move 
        
        measured_angle = system.read()
        print(measured_angle) #check what angle the arduino is at
        system.update_lcd(measured_angle)
        previous_angle = angle

    