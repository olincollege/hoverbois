#define left_fan_pin  0
#define right_fan_pin 1

#define c_pin 21
#define d_pin 20
#define a_pin 19
#define b_pin 18

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

#define _PWM_LOGLEVEL_        3
#include "RP2040_PWM.h"

//creates pwm instance
RP2040_PWM* left_fan;
//RP2040_PWM* right_fan;

float frequency;
float dutyCycle;


void setup()
{
  frequency = 25000;
  //assigns pin 25 (built in LED), with frequency of 20 KHz and a duty cycle of 0%
  left_fan = new RP2040_PWM(left_fan_pin, frequency, 0);
  //right_fan = new RP2040_PWM(right_fan_pin, frequency, 0);
  // dont have to pinmode for inputs
  left_fan->setPWM(left_fan_pin, frequency, 0);
//right_fan->setPWM(left_fan_pin, frequency, 0);
}

void loop()
{
  
left_fan->setPWM(left_fan_pin, frequency, 100*digitalRead(b_pin));
//right_fan->setPWM(left_fan_pin, frequency, 50*digitalRead(b_pin));

}
