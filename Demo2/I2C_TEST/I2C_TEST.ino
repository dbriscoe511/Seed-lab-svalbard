// see instructions in assignment2.py file for usage
#include <Wire.h>

#define PI 3.1415926535897932384626433832795 //definition for PI constant
#define LEFT_WHEEL_TARGET = 0
#define RIGHT_WHEEL_TARGET = 1
#define ANGLE_TARGET = 3

// PIN ASSIGNMENT
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

// ISR VARIABLES
volatile bool channelA1 = HIGH; //Channel A set on default
volatile bool channelB1 = HIGH; //Channel B set on default
volatile bool channelA2 = HIGH; //Channel A set on default
volatile bool channelB2 = HIGH; //Channel B set on default
volatile int count1 = 0; //counter variable for position
volatile int count2 = 0; //counter variable for position

// MAIN LOOP VARIABLES
unsigned long timeDelta = 0; //time in between loops
unsigned long timeMain = 0; //time loop takes place
float velocity1 = 0; //velocity of left wheel
float velocity2 = 0; //velocity of right wheel
float velocityForward = 0; //forward velocity of robot
float velocityAngular = 0; //angular velocity of robot
float positionForward = 0; //forward position of robot
float positionAngular = 0; //angular position of robot

// I2C VARIABLES
uint8_t c[10];
uint8_t state;



void setup() {
  Serial.begin(9600);        // start serial for output
  pinMode(channelA1Pin,INPUT_PULLUP);
  pinMode(channelB1Pin,INPUT_PULLUP);
  pinMode(channelA2Pin,INPUT_PULLUP);
  pinMode(channelB2Pin,INPUT_PULLUP);

  pinMode(voltageMotor1,OUTPUT);
  pinMode(voltageMotor2,OUTPUT);
  pinMode(signMotor1,OUTPUT);
  pinMode(signMotor2,OUTPUT);
  pinMode(statusFlag,INPUT);
  pinMode(enablePin,OUTPUT);
  digitalWrite(enablePin,HIGH);
  
  pinMode(powerPin,OUTPUT);
  digitalWrite(powerPin,HIGH);
  attachInterrupt(digitalPinToInterrupt(channelA1Pin), encoder1ISR, CHANGE); //sets interrupt to happen when channel A changes
  attachInterrupt(digitalPinToInterrupt(channelA2Pin), encoder2ISR, CHANGE);
  
  Wire.begin(4);             // join i2c bus with address #4
  Wire.onReceive(receive_e); // register event
  Wire.onRequest(sendData);
}
  
void loop() {
  timeDelta = micros()-timeMain; //time in between loops
  timeMain = micros(); //time of current loop

  velocity1 = (count1*2*PI*1000000.0)/(3200.0*timeDelta); //rotational velocity of wheel 1
  count1=0; //resets counts of wheel 1
  velocity2 = (count2*2*PI*1000000.0)/(3200.0*timeDelta); //rotational velocity of wheel 2
  count2=0; //resets counts of wheel 2
  velocityForward = (velocity1+velocity2)*(3.0/2.0); //forward velocity of robot
  velocityAngular = (velocity1-velocity2)*(3.0/11.0); //angular velocity of robot
  positionForward = positionForward+(velocityForward * timeDelta/1000000.0); //forward position of robot
  positionAngular = positionAngular+(velocityAngular * timeDelta/1000000.0); //angular position of robot

  
}
  
void receive_e(int events) {
  int i = 0;
  while(Wire.available()){
    c[i] = Wire.read();
    i++; // byte length of message (a length 1 message in this case is a data request. ignore)
  }
  //may need to disable pwm while these commands are being processed?
  if (i==2){
    if (c[0] == LEFT_WHEEL_VEL){
      state = VELOCITY_CNT;
      l_vel = ((c[1]-127)*(105.0/256));//0 to 255 becomes -127 to 127 and then is multiplied to reach a reasonable speed
    }
    else if (c[0] == RIGHT_WHEEL_VEL){
      state = VELOCITY_CNT;
      r_vel = ((c[1]-127)*(105.0/256));
    }
    else if (c[0] == ANGLE){
      state = ANGLE_CNT;
      a_vel = ((c[1]-127)*(105.0/256));
    } els e{
      Serial.println("invalid command")
      //print in interupt is bad practice, but it should be fine 
    }
  } else if (i>1){
     Serial.println("too long of a data string")
  } 
}

//void sendData() {
//  Wire.write(arr[2]);
//}


void encoder1ISR() { //interrupt for wheel 1 (left)
  channelA1 = digitalRead(channelA1Pin); //Reads channels for current iteration
  channelB1 = digitalRead(channelB1Pin);
  if (channelA1==channelB1){ //Adds to counter if channel A matches channel B
      count1=count1-2;      
  } else { //Subtracts from counter if channel A differs from channel B
      count1=count1+2;
  }
}

void encoder2ISR() { //interrupt for wheel 2 (right)
  channelA2 = digitalRead(channelA2Pin); //Reads channels for current iteration
  channelB2 = digitalRead(channelB2Pin);
  if (channelA2==channelB2){ //Adds to counter if channel A matches channel B
      count2=count2-2;      
  } else { //Subtracts from counter if channel A differs from channel B
      count2=count2+2;
  }
}
