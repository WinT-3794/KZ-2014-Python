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

import drive
import lifter
import shooter

class Kooz2014 (wpilib.IterativeRobot):        
    def robotInit (self):
        self.drive = drive.Drive()
        self.lifter = lifter.Lifter()
        self.shooter = shooter.Shooter()
        
        self.drive.setBrakeEnabled (True)
        self.shooter.setBrakeEnabled (True)
    
        self.drive.setSafetyEnabled (True)
        self.lifter.setSafetyEnabled (True)
        self.shooter.setSafetyEnabled (True)

    def teleopPeriodic (self):
        self.drive.moveWithJoystick (wpilib.Joystick (0))
        self.lifter.moveWithJoystick (wpilib.Joystick (1))
        self.shooter.moveWithJoystick (wpilib.Joystick (1))
        
if (__name__ == "__main__"):
    wpilib.run (Kooz2014)
