  // see instructions in assignment2.py file for usage
#define LEFT_WHEEL_VEL = 0
#define RIGHT_WHEEL_VEL = 1
#define DIST = 2
#define ANGLE = 3
  #include <Wire.h>
  uint8_t c[10];
  int arr[5]; // includes 
  uint8_t state;
  void setup()
  {
    Wire.begin(4);                // join i2c bus with address #4
    Wire.onReceive(receive_e); // register event
    Wire.onRequest(sendData);
    Serial.begin(9600);           // start serial for output
  }
  
  void loop()
  {
    delay(100);
  }
  
  void receive_e(int events)
  {
    int i = 0;
    while(Wire.available()){
      c[i] = Wire.read();
      i++; // byte length of message (a length 1 message in this case is a data request. ignore)
    }
    //may need to disable pwm while these commands are being processed?
    if (i==2){
      if (c[0] == LEFT_WHEEL_VEL){
        state = VELOCITY_CNT;
        l_vel = (c[1]-127)*VELOCITY_MULTIPLIER;//0 to 256 becomes -127 to 127 and then is multiplied to reach a reasonable speed
      }
      else if (c[0] == RIGHT_WHEEL_VEL){
        state = VELOCITY_CNT;
        r_vel = (c[1]-127)*VELOCITY_MULTIPLIER;
      }
      else if (c[0] == ANGLE){
        state = ANGLE_CNT;
        r_vel = (c[1]-127)*ANGLE_MULTIPLIER;
      }
      else{
        Serial.println("invalid command")
        //print in interupt is bad practice, but it should be fine 
      }

    } else if (i>1){
       Serial.println("too long of a data string")
    }
    //Serial.println(c);
    //Serial.println(arr);
    
    
  }
  void sendData()
  {
    Wire.write(arr[2]);
  }

    
