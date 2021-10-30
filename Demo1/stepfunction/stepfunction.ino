//this code is for collecting experimental data between the two motors

#define PI 3.1415926535897932384626433832795 //definition for PI constant

//Pin assignment and global variable instantiation
const int powerPin = 11; //pin for an extra Vcc = 5V
const int channelA1Pin = 2;
const int channelB1Pin = 5;
const int channelA2Pin = 3;
const int channelB2Pin = 6;

const int enablePin = 4; //Pin for enabling motor shield
const int voltageMotor1 = 9; //P in for voltage given to motor 1
const int voltageMotor2 = 10; //Pin for voltage given to motor 2 (not used)
const int signMotor1 = 7; //Pin for direction of motor 1
const int signMotor2 = 8; //Pin for direction of motor 2 (not used)
const int statusFlag = 12; //Pin for status flag


void setup() { //Sets up pins and serial monitor
  pinMode(voltageMotor1,OUTPUT); 
  pinMode(voltageMotor2,OUTPUT);
  pinMode(signMotor1,OUTPUT);
  pinMode(signMotor2,OUTPUT);
  pinMode(statusFlag,INPUT); //status flag input
  pinMode(enablePin,OUTPUT); //enable flag output
  digitalWrite(enablePin,HIGH); //sets enable flag high
}

void loop() {
  digitalWrite(signMotor1,HIGH); //direction of left motor
  digitalWrite(signMotor2,HIGH); //direction of right motor
  analogWrite(voltageMotor1,255); //writes PWM counts to motor 1
  //analogWrite(voltageMotor2,255); //writes PWM counts to motor 2
}
