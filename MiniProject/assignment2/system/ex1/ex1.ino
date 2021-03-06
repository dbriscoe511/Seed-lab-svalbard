+  #include <Wire.h>
  int c = 0; // used to store the value for i2c test
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
    
    c = Wire.read(); 
    Serial.println(c); // serial just used for debug
    
    c += 5;
    Serial.println(c);
    
  }
  void sendData()
  {
    Wire.write(c);
  }
    
