SEED Lab Team 5 - Svalbard Mini Project Read Me
Team Members:	Daniel Briscoe
		Peyton Rehl
		Kristen Ung
		Brian "X-Man" Bahr
		Beau Collins
**System Integration:** Send data between a RaspberryPi and Arduino using I2C
protocol in order to interface between computer vision and localization.

**Computer Vision:** Use openCV to detect and isolate blue painters tape on the ground,
and calculate how much the robot must turn to be centered with the tape.

**Localization:** Control the motors of the robot using an Arduino, telling the robot
to turn a certain amount or go foward a distance, using control systems to keep the robot
on track for following commands.

**Simulation and Control:** Create control system models in Simulink to upload the data read
by the motor encoders, and tune the system to ensure the robot performs the desired task.

This folder contains the materials needed for Demo1. 
Each folder in this demo folder contains an arduino script, which are individually commented.
The main.py contains the code that needs to be run to perform a comp vision demo,
the "forwardangularpositioncontroller" contains the code to perform the movement functions needed in the demo
