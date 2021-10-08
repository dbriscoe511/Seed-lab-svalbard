#include <Wire.h> //library for I2C communication

#define PI 3.1415926535897932384626433832795 //definition for PI constant

//Pin assignment
const int channelAPin = 2; //Pin for reading encoder channel A
const int channelBPin = 5; //Pin for reading encoder channel B
const int enablePin = 4; //Pin for enabling motor shield
const int voltageMotor1 = 9; //Pin for voltage given to motor 1
const int voltageMotor2 = 10; //Pin for voltage given to motor 2 (not used)
const int signMotor1 = 7; //Pin for direction of motor 1
const int signMotor2 = 8; //Pin for direction of motor 2 (not used)
const int statusFlag = 12; //Pin for status flag

//Variables used in encoder ISR
volatile bool channelA = HIGH; //Channel A set on default
volatile bool channelB = HIGH; //Channel B set on default
volatile int count = 0; //counter variable for position 

unsigned long lastTimeMeasured = 0; //measures time between loops
float desired = 0; //desired path, converted from msg
float radian = 0; //actual path, converted from encoder counts
float integral = 0; //integral path
float proportional = 0; //proportional path
float error = 0; //signal for difference between desired path and actual path
float Kp = 4; //constant for proportional control (volt/radian)
float Ki = 0; //constant for integral control (volt/radian)
int PWM = 35; //converts volts to PWM counts (PWM/volt)
byte msg =0; //msg for I2C communication

void setup() { //Sets up pins
  pinMode(channelAPin,INPUT_PULLUP);
  pinMode(channelBPin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(channelAPin), encoderISR, CHANGE); //sets interrupt to happen when channel A changes
  pinMode(enablePin,OUTPUT);
  pinMode(voltageMotor1,OUTPUT);
  pinMode(signMotor1,OUTPUT);
  pinMode(statusFlag,INPUT);
  digitalWrite(enablePin,HIGH); //enables motor shield

  Wire.begin(4);             // join i2c bus with address #4
  Wire.onReceive(receive_e); // register event
  Wire.onRequest(sendData);
}

void loop() { //main loop
  desired = msg*(PI/2.0); //converts msg into the desired position
  radian = ((count/3200.0)*2*PI); //converts encoder counts into the actual position
  
  error = desired - radian; //error path (rad)

  if(error > 0){
    digitalWrite(signMotor1,HIGH); //sets direction clockwise if the error is positive (its not far enough)
  } else if (error < 0){
    digitalWrite(signMotor1,LOW); //sets direction counterclockwise if the error is negative (its too far)
  }

  integral = integral + (error*((millis()-lastTimeMeasured)/1000.0)); //integral path (rad)
  proportional = (Kp*error)+(Ki*integral); //proportional path (volts)
  PWM = int(proportional*35); //converts volts into PWMs (1v=35pwm)

  if(abs(PWM)>255){ //saturates PWM and caps at 255
    PWM = 255;
  }

  analogWrite(voltageMotor1,abs(PWM)); //writes PWM counts to motor 1
}

void encoderISR() { //interrupt for encoder
  channelA = digitalRead(channelAPin);
  channelB = digitalRead(channelBPin);
  if (channelA==channelB){ //clockwise if channels are equal
    count+=2;
  } else { //counterclockwise if channels are different
    count-=2;
  }
}

void receive_e(int events) //receive function
{
  msg = Wire.read();
}

void sendData() //send function
{
  Wire.write(msg);
}
