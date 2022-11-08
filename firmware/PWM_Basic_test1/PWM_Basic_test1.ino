#include <Servo.h>



//creates pwm instance
Servo esc1;
Servo esc2;
Servo steer_motor;

#define fpin      1
#define spin      2
#define hpin      5

void setup()
{
  Serial.begin(115200);
  esc1.attach(fpin);
  esc2.attach(hpin);
  steer_motor.attach(spin);
}
int speedf=0;
int speedfnow = 0;
int steer=0;
int speedh=0;
int speedhnow = 0;
void loop()
{
  int rawf = 0;
  int raws = 0;
  int rawh = 0;
  
  while(Serial.available()==0){
  
  }
  while(Serial.available()>0){
   char a = Serial.read();
   if(a=='h'){
    rawh = max(Serial.parseInt(),rawh);
    speedh = rawh;
   }
   if(a=='f'){
    rawf = max(Serial.parseInt(),rawf);
    speedf = rawf;
   }
   if(a=='s'){
    raws = max(Serial.parseInt(),raws);
    steer = raws;
   }
  }
  Serial.print(steer);
  Serial.print(",");
  Serial.print(speedf);
  Serial.print(",");
  Serial.println(speedh);
  steer_motor.write(steer);
  //speedfnow+= 1;
  //speedfnow = min(speedfnow,speedf);
  //speedhnow+= 1;
  //speedhnow = min(speedhnow,speedh);
  esc1.write(speedf);
  esc2.write(speedh);
  //delay(2);

}
