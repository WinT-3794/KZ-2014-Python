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

class Lifter:
    def __init__ (self):
        self.Lifter = wpilib.VictorSP (constants.Lifter)
        
    def setSafetyEnabled (self, enabled):
        self.Lifter.setSafetyEnabled (enabled)
        
    def move (self, speed):
        self.Lifter.set (constants.RemoveDeadband (speed))
    
    def moveWithJoystick (self, joystick):
        if joystick.getRawButton (5):
            self.moveLifter (constants.MaximumMotorOutput)

        elif joystick.getRawButton (6):
            self.moveLifter (constants.MaximumMotorOutput * -1)
