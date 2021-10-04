#define PI 3.1415926535897932384626433832795

//Pin assignment and global variable instantiation
const int channelAPin = 2;
const int channelBPin = 4;
volatile bool channelA = HIGH; //Channel A set on default
volatile bool channelB = HIGH; //Channel B set on default
volatile int count = 0; //counter variable for position 
unsigned long lastTimeMeasured = 0;
int degree = 0;
float radian = 0;
float velocity = 0;
byte msg = 0;

void setup() { //Sets up pins and serial monitor
  Serial.begin(115200);
  pinMode(channelAPin,INPUT_PULLUP);
  pinMode(channelBPin,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(channelAPin), encoderISR, CHANGE); //sets interrupt to happen when channel A changes

  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receive_e); // register event
  Wire.onRequest(sendData);
}

void loop() { //main loop
  if((millis()-lastTimeMeasured)>10){
    degree = count/9;
    velocity = ((count/(3200.0/(2*PI)))-radian)/.01;
    radian = count/(3200.0/(2*PI));
    
    Serial.print(millis()/1000.0);
    Serial.print("\t");
    Serial.print(count);
    //Serial.print("counts   ");
    Serial.print("\t");
    //Serial.print(degree);
    //Serial.print("degrees   ");
    Serial.print(radian,3);
    Serial.print("\t");
    //Serial.print("radians   ");
    Serial.print(velocity);
    //Serial.println("rad/s");
    Serial.println();
    
    lastTimeMeasured = millis();
    }
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
