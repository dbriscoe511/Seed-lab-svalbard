# SEED Lab Team 5 - Svalbard Read Me

## Team Members: Daniel Briscoe, Peyton Rehl, Kristen Ung, Brian "X-Man" Bahr, Beau Collins

This repository contains code for the Colorado School of Mines EENG350 Seed Lab Class.

The purpose of this class is to design and build a robot that can track and follow a
trail of blue painter's tape on the ground. The project is split into the following
subsystems with different tasks and responsibilities:

**System Integration:** Send data between a RaspberryPi and Arduino using I2C
protocol in order to interface between computer vision and localization.

**Computer Vision:** Use openCV to detect and isolate blue painters tape on the ground,
and calculate how much the robot must turn to be centered with the tape.

**Localization:** Control the motors of the robot using an Arduino, telling the robot
to turn a certain amount or go foward a distance, using control systems to keep the robot
on track for following commands.

**Simulation and Control:** Create control system models in Simulink to upload the data read
by the motor encoders, and tune the system to ensure the robot performs the desired task.
