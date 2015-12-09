#!/usr/bin/env python3

#
# Copyright (c) WinT 3794 <http://wint3794.org>
#
# This is free and open source software, you are welcome to use, share and
# modify it under the terms of the DBAD license.
# For more information, check the LICENSE file in the root directory of
# this project.
#

import wpilib
import constants

class Shooter:
    def __init__ (self):
        self.Shooter_A = wpilib.CANTalon (constants.Shooter_A)
        self.Shooter_B = wpilib.CANTalon (constants.Shooter_B)
        
    def setSafetyEnabled (self, enabled):
        self.Shooter_A.setSafetyEnabled (enabled)
        self.Shooter_B.setSafetyEnabled (enabled)
        
    def setBrakeEnabled (self, enabled):
        self.Shooter_A.enableBrakeMode (enabled)
        self.Shooter_B.enableBrakeMode (enabled)
        
    def move (self, speed):
        self.Shooter_A.set (constants.RemoveDeadband (speed))
        self.Shooter_B.set (constants.RemoveDeadband (speed))
    
    def moveWithJoystick (self, joystick):
        speed = 0
        left = joystick.getRawAxis (2)
        right = joystick.getRawAxis (3)

        if left > right:
            speed = left
        elif right > left:
            speed = right * -1

        self.move (speed)
