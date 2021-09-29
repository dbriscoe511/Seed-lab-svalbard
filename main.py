import time
import comms
#import computer_vision 

previous_angle = 1
system = comms.comm()
while True:
    #check comp vision, get angle

    angle = int(input("enter angle"))
    measured_angle = 0
    time.sleep(0.5)

    if not angle == previous_angle:
        print("sending...")
        if(angle-previous_angle>0):
            encoderangle = (angle-previous_angle)
        else:
            encoderangle = (angle-previous_angle+4)%4

        
        system.send(angle)
        
        measured_angle = system.read()
        system.update_lcd(measured_angle)
        previous_angle = angle

    