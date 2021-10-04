import time
import comms
import miniproj_cv as mcv

previous_angle = 1
system = comms.comm()
camera = mcv.setup_camera()
camera = mcv.calibrate(camera)

while True:
    #check comp vision, get angle

    #angle = int(input("enter angle"))
    t_angle = mcv.capture_angle(camera)
    print(str(t_angle)+'\n\n\n')
    if(t_angle>90):
        angle = 4
    elif(t_angle>0):
        angle = 3
    elif(t_angle>-90):
        angle = 2
    else:
        angle = 1

    measured_angle = 0
    time.sleep(0.5)

    if not angle == previous_angle:
        print("sending...")
        if(angle-previous_angle>0):
            encoderangle = (angle-previous_angle)
        else:
            encoderangle = (angle-previous_angle+4)%4

        
        system.send(int(angle))
        
        measured_angle = system.read()
        print(measured_angle)
        system.update_lcd(measured_angle)
        previous_angle = angle

    