  // see instructions in assignment2.py file for usage
  #include <Wire.h>
  int c[32];
  int arr[5]; // includes 
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
      i++;
    }
    i--; // corrects length because SMBus uses a blank byte during data send 
    if i==1{
      arr[c[0]] = c[1]; // sets arr at offset(c[0]) to value (c[1])
    }
    //Serial.println(c);
    //Serial.println(arr);
    
    
  }
  void sendData()
  {
    Wire.write(arr[2]);
  }

    
