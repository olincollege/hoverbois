---
title: Electrical
menu:
  navbar:
    weight: 40
---

TODO: Insert circuit schematics, photos, descriptions

# Electrical System

We designed the electrical subsystem to integrate as easily with the software
systems as possible. Thus, everything was accessible under an easy to use
Python "driver" interface as described in the [Software]({{< ref
"/docs/software/" >}}) portion of the website. In addition, we made the final
design found in Sprint 3 as tightly integrated with the [Mechanical]({{< ref
"/docs/mechanical/" >}}) system after a near tragic accident during Sprint 2.

## Power Delivery

## Computer

The electrical subsystem is the designed around a Raspberry Pi 3B+ (upgraded
from Sprint 1's Pi 2) and a Raspberry Pi Pico microcontroller. The two
communicate over USB. Using a microcontroller in addition to a single board
computer has the following advantages:
- **The Raspberry Pi 3B+ technically has 4 PWM pins but only 2 PWM channels.
  Thus, we can only generate 2 of the 3 PWM signals we required for motor
  control.**
- It improves software performance. The Pico handling the motor control frees
  up CPU time to run more sophisticated controllers.

## Motors

Talk about ESCs

## Servo

Talk about servo

## Peripherals

Talk about IMU and GPS. I²C
