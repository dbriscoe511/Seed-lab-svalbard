#define PI 3.1415926535897932384626433832795 //definition for PI constant

//Pin assignment and global variable instantiation
const int powerPin = 11;
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

//ISR variables
volatile bool channelA1 = HIGH; //Channel A set on default
volatile bool channelB1 = HIGH; //Channel B set on default
volatile bool channelA2 = HIGH; //Channel A set on default
volatile bool channelB2 = HIGH; //Channel B set on default
volatile int count1 = 0; //counter variable for position
volatile int count2 = 0; //counter variable for position

//main loop variables
unsigned long timeDelta = 0;
unsigned long timeMain = 0;
float velocity1 = 0;
float velocity2 = 0;
float velocityForward = 0;
float velocityAngular = 0;
float positionForward = 0;
float positionAngular = 0;

float errorAngular = 0;
float desiredAngular = 0.24434612519895391;
float integralAngular = 0;
float KpAngular = 15; //constant for proportional control (volt/radian)
float KiAngular = 0.1; //constant for integral control (volt/radian)

int PWM = 255;

int OldPWM = 0;

int PWM1 = 0;
int PWM2 = 0;


void setup() { //Sets up pins and serial monitor
  Serial.begin(9600);
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
}

void loop() { //main loop (nothing)
  timeDelta = micros()-timeMain;
  timeMain = micros();

  velocity1 = (count1*2*PI*1000000.0)/(3200.0*timeDelta); //rotational velocity of wheel 1
  count1=0;
  velocity2 = (count2*2*PI*1000000.0)/(3200.0*timeDelta); //rotational velocity of wheel 2
  count2=0;
  velocityForward = (velocity1+velocity2)*(3.0/2.0); //forward velocity of robot
  velocityAngular = (velocity1-velocity2)*(3.0/11.0); //angular velocity of robot
  positionForward = positionForward+(velocityForward * timeDelta/1000000.0);
  positionAngular = positionAngular+(velocityAngular * timeDelta/1000000.0);
  
  errorAngular = (desiredAngular - positionAngular);
    if(errorAngular > 0){
      digitalWrite(signMotor1,HIGH); //sets direction clockwise if the error is positive (its not far enough)
      digitalWrite(signMotor2,HIGH);
    } else if (errorAngular < 0){
      digitalWrite(signMotor1,LOW); //sets direction counterclockwise if the error is negative (its too far)
      digitalWrite(signMotor2,LOW);
    }
  integralAngular = integralAngular + (errorAngular * timeDelta / 1000000.0); //integral path (rad)
  errorAngular = (KpAngular*errorAngular)+(KiAngular*integralAngular); //proportional path (volts)
  PWM = int(errorAngular*52); //converts volts into PWMs (1/2v=17pwm)

  if ((PWM-OldPWM) > 70) {
    PWM = OldPWM+70;
  }
  if ((PWM-OldPWM) < -70){
    PWM = OldPWM-70;
  }

  PWM1 = PWM;
  PWM2 = (PWM * 19.5)/17;

  if(abs(PWM2)>255){ //saturates PWM and caps at 255
    PWM2 = 255;
    PWM1 = (255 * 17)/19.5;
  }

  analogWrite(voltageMotor1,abs(PWM1)); //writes PWM counts to motor 1
  analogWrite(voltageMotor2,abs(PWM2));  
  
  Serial.print("velocity1: ");
  Serial.print(velocity1);
  Serial.print("\tvelocity2: ");
  Serial.print(velocity2);
  Serial.print("\tvelocityForward: ");
  Serial.print(velocityForward);
  Serial.print("\tvelocityAngular: ");
  Serial.println(velocityAngular);
  Serial.print("positionForward: ");
  Serial.print(positionForward);
  Serial.print("\tpositionAngular: ");
  Serial.println(positionAngular);
  Serial.println();
}

void encoder1ISR() { //interrupt
  channelA1 = digitalRead(channelA1Pin); //Reads channels for current iteration
  channelB1 = digitalRead(channelB1Pin);
  if (channelA1==channelB1){ //Adds to counter if channel A matches channel B
      count1=count1-2;      
  } else { //Subtracts from counter if channel A differs from channel B
      count1=count1+2;
  }
}

void encoder2ISR() { //interrupt
  channelA2 = digitalRead(channelA2Pin); //Reads channels for current iteration
  channelB2 = digitalRead(channelB2Pin);
  if (channelA2==channelB2){ //Adds to counter if channel A matches channel B
      count2=count2-2;      
  } else { //Subtracts from counter if channel A differs from channel B
      count2=count2+2;
  }
}
