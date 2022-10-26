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
RP2040_PWM* PWM_Instance;

float frequency;
float dutyCycle;

#define pinToUse      1

void setup()
{
  //assigns pin 25 (built in LED), with frequency of 20 KHz and a duty cycle of 0%
  PWM_Instance = new RP2040_PWM(pinToUse, 25000, 0);
  Serial.begin(115200);
  PWM_Instance->setPWM(pinToUse, 25000, 0);
}
int speed=0;
void loop()
{
  int raw = 0;
  while(Serial.available()==0){}
  while(Serial.available()>0){
   raw = max(Serial.parseInt(),raw);
  }
  //Serial.println(raw);
  speed = raw;
  frequency = 25000;

  PWM_Instance->setPWM(pinToUse, frequency, speed);

}
