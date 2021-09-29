  #include <Wire.h>
  int c = 0;
  void setup()
  {
    Wire.begin(4);                // join i2c bus with address #4
    Wire.onReceive(receive_e); // register event
    Wire.onRequest(sendData);
    Serial.begin(115200);           // start serial for output
  }
  
  void loop()
  {
    delay(100);
  }
  
  void receive_e(int events)
  {
    c = Wire.read();
    Serial.println(c);
  }
  void sendData()
  {
    Wire.write(c);
  }
    
