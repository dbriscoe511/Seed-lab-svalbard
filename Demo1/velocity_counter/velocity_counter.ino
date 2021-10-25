

#define PI 3.1415926535897932384626433832795 //definition for PI constant

//Pin assignment and global variable instantiation
const int powerPin = 11;
const int channelA1Pin = 2;
const int channelB1Pin = 5;
const int channelA2Pin = 3;
const int channelB2Pin = 6;

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



void setup() { //Sets up pins and serial monitor
  Serial.begin(9600);
  pinMode(channelA1Pin,INPUT_PULLUP);
  pinMode(channelB1Pin,INPUT_PULLUP);
  pinMode(channelA2Pin,INPUT_PULLUP);
  pinMode(channelB2Pin,INPUT_PULLUP);

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