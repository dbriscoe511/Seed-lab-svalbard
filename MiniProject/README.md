SEED Lab Team 5 - Svalbard Mini Project Read Me
Team Members:	Daniel Briscoe
		Peyton Rehl
		Kristen Ung
		Brian "X-Man" Bahr
		Beau Collins

How to run the project:
In order to run the Mini Project, the user needs to load both the main.py code to the Raspberry Pi and the mini_proj.ino to the Arduino. Once both programs are loaded, the camera will take some time to calibrate and then will begin catpuring images. The main.py terminal will display the 1-4 value that will be sent to the Arduino, and the arduino will execute code to move the wheel. The direction of movement is determined by the new numbering position, and the previous value.

The battery voltage is displayed on a separate LCD display. A lower threshold of 7.4 V is set to prevent the functionality of the control system from changing due to lower voltage.
