  #include <Wire.h>
  byte c[32]; //stores raw i2c message
 
  byte data[32];// stores reversed str
  int dln; // data string length
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
      c[i] = ( Wire.read());
      i++;
    }
    i--;
    if(i>1){ //make sure this is an entry, not a request
      dln = i; // length of the string gets stored
      Serial.println(i);
      for(int j =0;j<i;j++){
        data[j] = c[i-j]; //iiterates trough the string backwards 
        Serial.println(c[i-j]);// prints the string (byte representation) backwards
      }
    } 
    Serial.println("recived data");
    //Serial.println(c);
    //Serial.println(arr);
    
    
  }
  void sendData()
  {
    
    Wire.write(data,dln);
    Serial.println("sent");
  }
  
    
