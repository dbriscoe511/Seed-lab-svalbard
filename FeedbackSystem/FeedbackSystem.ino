#include <Wire.h>

#define PI 3.1415926535897932384626433832795

//Pin assignment and global variable instantiation
const int channelAPin = 2; 
const int channelBPin = 5;
const int enablePin = 4;
const int voltageMotor1 = 9;
const int voltageMotor2 = 10;
const int signMotor1 = 7;
const int signMotor2 = 8;
const int statusFlag = 12;

volatile bool channelA = HIGH; //Channel A set on default
volatile bool channelB = HIGH; //Channel B set on default
volatile int count = 0; //counter variable for position 
unsigned long lastTimeMeasured = 0;

float desired = 0;
float radian = 0;
float integral = 0;
float proportional = 0;
float error = 0;
float Kp = 1.1; //1.1
float Ki = 0.34;

int PWM = 35;
byte msg =0;

void setup() { //Sets up pins and serial monitor
  Serial.begin(9600);
  pinMode(channelAPin,INPUT_PULLUP);
  pinMode(channelBPin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(channelAPin), encoderISR, CHANGE); //sets interrupt to happen when channel A changes
  pinMode(enablePin,OUTPUT);
  pinMode(voltageMotor1,OUTPUT);
  pinMode(signMotor1,OUTPUT);
  pinMode(statusFlag,INPUT);
  digitalWrite(enablePin,HIGH);

  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receive_e); // register event
  Wire.onRequest(sendData);
}

void loop() { //main loop
desired = msg*(PI/2.0);

radian = ((count/3200.0)*2*PI);
error = desired - radian;
if(error > 0){
  digitalWrite(signMotor1,HIGH);
} else if (error < 0){
  digitalWrite(signMotor1,LOW);
}

integral = integral + (error*((millis()-lastTimeMeasured)/1000.0));
proportional = (Kp*error)+(Ki*integral);
PWM = int(proportional*35);
if(abs(PWM)>255){
  PWM = PWM % 255;
}
analogWrite(voltageMotor1,PWM);
}

void encoderISR() { //interrupt
  channelA = digitalRead(channelAPin);
  channelB = digitalRead(channelBPin);
  if (channelA==channelB){
    count+=2;
  } else {
    count-=2;
  }
}

void receive_e(int events)
{
  msg = Wire.read();
  Serial.println(msg);
}
void sendData()
{
  Wire.write(msg);
}
