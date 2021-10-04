  #include <Wire.h>
  int c = 0;
  byte adcdatah,adcdatal; // stores the two bytes of adc data
  bool fsent = false; // used to see if the first or second byte should be transmitted
  void setup()
  {
    Wire.begin(4);                // join i2c bus with address #4
    Wire.onReceive(receive_e); // register event
    Wire.onRequest(sendData);
    Serial.begin(9600);           // start serial for output
  }
  
  void loop()
  {
    delay(500);
    int dat = analogRead(A1); // updates the analog value read in
    adcdatah =highByte(dat); // stores the analog value in high and low bytes
    adcdatal =lowByte(dat);
  }
  
  void receive_e(int events)
  {
    c = Wire.read(); // needs to be able to read data to not throw errors if data is sent. 
    Serial.println("not used");
 
    
  }
  void sendData()
  {
    if(fsent){
      Wire.write(adcdatal);
    }else{
      Wire.write(adcdatah);
    }
    fsent = !fsent; // sends the next part of the adc data when it is requested
  }
    
