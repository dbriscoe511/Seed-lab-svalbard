const int enablePin = 4;
const int voltageMotor1 = 9;
const int voltageMotor2 = 10;
const int signMotor1 = 7;
const int signMotor2 = 8;
const int statusFlag = 12;

void setup() {
  pinMode(enablePin,OUTPUT);
  pinMode(voltageMotor1,OUTPUT);
  pinMode(signMotor1,OUTPUT);
  pinMode(statusFlag,INPUT);
  digitalWrite(enablePin,HIGH);
}

void loop() {
  analogWrite(voltageMotor1,1);
  digitalWrite(signMotor1,HIGH);
}
