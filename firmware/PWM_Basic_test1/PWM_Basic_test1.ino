#include <Servo.h>

/****************************************************************************************************************************
  basic_pwm.ino
  For RP2040 boards
  Written by Dr. Benjamin Bird

  A basic example to get you up and running.

  Library by Khoi Hoang https://github.com/khoih-prog/RP2040_PWM
  Licensed under MIT license

  The RP2040 PWM block has 8 identical slices. Each slice can drive two PWM output signals, or measure the frequency
  or duty cycle of an input signal. This gives a total of up to 16 controllable PWM outputs. All 30 GPIO pins can be driven
  by the PWM block
*****************************************************************************************************************************/

//#define _PWM_LOGLEVEL_        0
#include "RP2040_PWM.h"

//creates pwm instance
RP2040_PWM* PWMf;
Servo esc1;
Servo esc2;
Servo steer_motor;
float frequency;
float dutyCycle;

#define fpin      1
#define spin      2
#define hpin      0

void setup()
{
  //assigns pin 25 (built in LED), with frequency of 20 KHz and a duty cycle of 0%
  //PWMf = new RP2040_PWM(fpin, 50, 0);
  //PWMs = new RP2040_PWM(spin, 50, 0);
  Serial.begin(115200);
  esc1.attach(fpin);
  esc1.attach(hpin);
  steer_motor.attach(spin);
  //PWMs->setPWM(spin, 50, 0);
  //PWMf->setPWM(fpin, 50, 0);
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
  
  while(Serial.available()==0){}
  while(Serial.available()>0){
   char a = Serial.read();
   if(a=='f'){
    rawf = max(Serial.parseInt(),rawf);
  speedf = rawf;
   }
   if(a=='h'){
    rawh = max(Serial.parseInt(),rawh);
  speedh
   }
   if(a=='s'){
    raws = max(Serial.parseInt(),raws);
  steer = raws;
   }
  }
  speedfnow+= 1;
  speedfnow = min(speedfnow,speedf);
  speedhnow+= 1;
  speedhnow = min(speedhnow,speedh);
  
  frequency = 50;
  Serial.print(steer);
  Serial.print(",");
  Serial.print(speedf);
  Serial.print(",");
  Serial.println(speedh);
  //PWMf->setPWM(fpin, frequency, speedf);
  //PWMs->setPWM(spin, 50, steer);
  esc1.write(speedf);
  esc2.write(speedh);
  steer_motor.write(steer);
  delay(2);

}
