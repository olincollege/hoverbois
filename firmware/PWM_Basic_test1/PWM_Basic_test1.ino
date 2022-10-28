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
Servo steer_motor;
float frequency;
float dutyCycle;

#define fpin      1
#define spin      0

void setup()
{
  //assigns pin 25 (built in LED), with frequency of 20 KHz and a duty cycle of 0%
  PWMf = new RP2040_PWM(fpin, 25000, 0);
  //PWMs = new RP2040_PWM(spin, 50, 0);
  Serial.begin(115200);
  steer_motor.attach(spin);
  //PWMs->setPWM(spin, 50, 0);
  PWMf->setPWM(fpin, 25000, 0);
}
int speedf=0;
int steer=0;
void loop()
{
  int rawf = 0;
  int raws = 0;
  while(Serial.available()==0){}
  while(Serial.available()>0){
   char a = Serial.read();
   if(a=='f'){
    rawf = max(Serial.parseInt(),rawf);
  speedf = rawf;
   }
   if(a=='s'){
    raws = max(Serial.parseInt(),raws);
  steer = raws;
   }
  }
  //Serial.println(raw);
  //speedf = rawf;
  //steer = raws;
  frequency = 25000;
  Serial.print(steer);
  Serial.print(",");
  Serial.println(speedf);
  PWMf->setPWM(fpin, frequency, speedf);
  //PWMs->setPWM(spin, 50, steer);
  steer_motor.write(steer);

}
