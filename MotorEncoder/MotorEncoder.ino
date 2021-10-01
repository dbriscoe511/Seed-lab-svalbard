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
int degree = 0;
float radian = 0;
float velocity = 0;
float voltage = 0;
int PWM = 35;

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
}

void loop() { //main loop
  if((millis()-lastTimeMeasured)>10){
    degree = count/9;
    velocity = ((count/(3200.0/(2*PI)))-radian)/.01;
    radian = count/(3200.0/(2*PI));
    voltage = ((PWM/255.0)*7.2);
    
    Serial.print(millis()/1000.0);
    Serial.print("\t");
    Serial.print(voltage);
    Serial.print("\t");
    Serial.println(velocity);
    
    lastTimeMeasured = millis();
  }
  analogWrite(voltageMotor1,PWM);
  digitalWrite(signMotor1,HIGH);
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
