---
title: Software
menu:
  navbar:
    weight: 50
---

# Hoverbot Software Development

This page describes the history of our hovercraft software (called
hovercraftpy) through our three design sprints. To view the code, please
checkout our repository on [GitHub](https://github.com/olincollege/hoverbois).

## Architecture Overview

The brain of the hovercraft is powered by a Raspberry Pi 3. All of the software
is written in Python. The components running on the Raspberry Pi are broken up
into `controllers` and `drivers`.

Controller modules exist to run the hovercraft's control loop:
1. Read user input. Different versions of the controller module exist to read
   different forms of input (web requests, bluetooth, USB radio).
2. Act on user input to update state
3. Send state to motor driver

Driver modules exists to interface with external devices using protocols such
as USB, SPI, and I²C. These devices include the Pi Pico, the IMU, and the GPS.
Drivers were based on an abstract base class called `HovercraftDriver`.

{{< img "images/software-diagram.png" "Block diagram of software architecture."
>}}

Additional features and versions of drivers and controllers were added across
sprints.

### Sprint 1

You can checkout the `end-of-sprint1` branch to view the software from this
sprint.

* Implemented a web-server based controller using
  [Tornado](https://www.tornadoweb.org/en/stable/). The Raspberry Pi hosted a
  simple website that allowed a user to send commands to the hovercraft.

* Implemented a [pySerial](https://github.com/pyserial/pyserial) based driver
  to talk to the Pi Pico [firmware](#firmware). We used this driver to control
  the thrust fan and the rudder.

{{< img "images/web-controller.png" "Screenshot of web controller website." >}}

Screenshot of web controller website. The website listens to keyboard presses
and sends requests back to the Raspberry Pi.

### Sprint 2

You can checkout the `sprint2` branch to view the software from this sprint.

* Refactored the codebase to use a proper Python project manager. Running
  Python files directly with `python` limits the project to a single directory
  as and makes it hard to manage dependencies. We ended up settling on
  [Poetry](https://python-poetry.org/) for its ease of use.

* Extended the web controller allow control of the newly added hover motor.

* Wrote a driver to talk to an IMU. This gave us access to accelerometer,
  gyroscope, and magnetometer data.

* Wrote a PID motor driver. This driver makes use of the original motor driver
  (now extended to control hover motor) and the IMU driver. The PID loop takes
  control of the hovercraft is told to not steer, and continuously adjusts the
  rudder angle to bring angular velocity to zero.

### Sprint 3

This is the state of the `main` branch.

* Implemented a Bluetooth controller module. This module reads input from a
  Bluetooth gamepad (specifically a Wii U Pro Controller), giving us access to
  analog rudder control. This runs on the Raspberry Pi.

* Extended web controller with a new request to receive analog controller data.

* Wrote [pygame](https://www.pygame.org/news) based applet to send web requests
  from a different computer. This circumvents the need for the clunky website
  and allows for analog control. In addition, this applet is extendable to use
  another form of control, such as a USB radio module. This runs on a separate
  laptop PC.

* We started having issues with pySerial, resulting in an unacceptable input
  delay of over a second. Unable to find the cause or a solution, we
  implemented a non-ideal workaround using a system call to write to the serial
  port. Unfortunately, using this method sometimes results in glitchy behavior
  if the motor state is updated too frequently, making the PID driver unusable.

{{< img "images/robot-gui.gif" "GIF animation of Pygame robot gui." >}}

## Discord Bot

We needed to obtain the Raspberry Pi's local IP address to access the Raspberry
Pi over ssh and to control over http. Considering how our team already
communicated over Discord, we opted to write a Discord bot that would print the
Pi's IP to the chat. We also wrote a systemd unit file to start the Discord bot
on the Pi's boot. This bot served its purpose for the entirety of the project.

## Firmware {#firmware}

The motors were driven by a Raspberry Pi Pico microcontroller (see
[electrical]({{< ref "docs/electrical" >}}) for details).

The firmware reads the Pi Pico's serial buffer, parsing for commands in a
gcode-like format. Commands tell the Pico to update the speed of the motors and
the angle of the rudder servo. For some reason, the Pico read each command
twice, always once with an argument of zero. We solved this issue with a unique
bug fix: read a command twice before an action, and pick the higher value of
the two. This ensured that each operation was not immediately undone.

The firmware was the least changed part of the project across the design
sprints.

- Sprint 1: Controlled thrust motor and rudder servo.
- Sprint 2: Added control for hover motor.
- Sprint 3: Unchanged
