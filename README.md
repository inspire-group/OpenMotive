# carwatch

## AMBER safety application for internet-connected vehicles

This program takes a vehicle license plate as an input and checks the camera for any plate that matches.
It has 3 modes:
- Raspberry Pi: all the computation is done on the raspberry pi,
- Cloud: all the computation is done on the cloud,
- Both: the computation is efficiently divided between the raspberry pi and the cloud.

## OBDII Private and Secure Relay Application

This program relays information from the vehicle OBDII port to any OBDII device in two modes:
- Standard: relay the information from the vehicle exactly as it was received.
- Secure: use data shuffling to stop private information leakage while keeping any OBDII device fully functional.

## Vehicle Transmission Sports and Efficiency Modes Upgrade

This program provides the user with knowledge about the optimal Engine RPMs at which
the vehicle must switch gears for maximum acceleration (Sports Mode) and at which the
vehicle must drive for maximum fuel efficiency (Efficiency Mode).

There are 2 phases: training and testing.
- During the training phase, the user will be asked to switch gears and drive at
specific Engine RPMs in order for the program to extract the RPM data combined
with the speed and fuel consumption. The program will then determine the optimal
values for Sports Mode and Efficiency Mode.
- During the testing phase, the user will automatically be given the optimal
Engine RPMs at which the vehicle must be driven for optimal functionality in
each mode.
