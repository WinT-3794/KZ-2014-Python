#!/usr/bin/env python3

#
# Copyright (c) WinT 3794 <http://wint3794.org>
#
# This is free and open source software, you are welcome to use, share and
# modify it under the terms of the DBAD license.
# For more information, check the LICENSE file in the root directory of
# this project.
#

# Define motor output ranges
MaximumMotorOutput = 0.85
MinimumMotorOutput = 0.15

# Define CAN Controller IDs
DriveFL_A = 4
DriveRL_A = 1
DriveFR_A = 5
DriveRR_A = 10
DriveFL_B = 3
DriveRL_B = 2
DriveFR_B = 6
DriveRR_B = 9
Shooter_A = 7
Shooter_B = 8

# Define PWM Controller IDs
Lifter = 0

# Ensures that the input value stays withing the motor output range
def RemoveDeadband (input):
    if input < MinimumMotorOutput:
        return 0
    
    elif input > MaximumMotorOutput:
        return MaximumMotorOutput * (input / abs (input))
        
    else:
        return input
