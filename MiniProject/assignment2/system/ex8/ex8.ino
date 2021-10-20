  #include <Wire.h>
  String  c = "";
  void setup()
  {
    Serial.begin(115200);           // start serial for output
  }
  
  void loop()
  {
    delay(100);
  }
  
  void serialEvent()
  {
    if(Serial.available()>0){ //when a serial inoput is recived this reads the input
      c = Serial.readStringUntil('\n');
      
    }
    Serial.flush(); // gets rid of crap in the serial buffer
    
    
    int i = c.toInt()+5; //converts the serial message to an int and adds 5. 
    delay(200);
    Serial.println(i);
    
  }
 
    
