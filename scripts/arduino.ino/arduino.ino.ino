#include <Servo.h>


Servo myservo;
float currpos = 0;
float targetpos = 20;
int i=0;
float inc =0.2;
int pos[2][2] ={{70,35},{0,35}};
int indpos = 0;
int selectpos =0;
int32_t v=0xffff0000;
void setup() {
  Serial.begin(9600);
  myservo.attach(7);
  myservo.write(0);
}

// the loop function runs over and over again forever
void loop() {
  *(int16_t*)&v = analogRead(0);
  Serial.write((char*)&v,4);
  if (Serial.available() > 0)
  {
    char c = Serial.read();
    if(c=='#')
      targetpos=20;  
    else if(c=='a')
      targetpos=80;  
  }
  if(targetpos-inc>currpos)
  {
    currpos+=inc;
  }
  else if(targetpos+inc<currpos)
  {
    currpos-=inc;
  }
//  else 
//  {
//    
//    indpos = (indpos+1)%2;
//    targetpos = pos[selectpos][indpos];
//  }
  myservo.write(currpos);
  
  delay(5);                       // wait for a second
}
