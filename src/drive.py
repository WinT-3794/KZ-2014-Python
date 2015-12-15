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

class Drive:
    def __init__ (self):
        self.FL_A = wpilib.CANTalon (constants.DriveFL_A)
        self.RL_A = wpilib.CANTalon (constants.DriveRL_A)
        self.FR_A = wpilib.CANTalon (constants.DriveFR_A)
        self.RR_A = wpilib.CANTalon (constants.DriveRR_A)
        self.FL_B = wpilib.CANTalon (constants.DriveFL_B)
        self.RL_B = wpilib.CANTalon (constants.DriveRL_B)
        self.FR_B = wpilib.CANTalon (constants.DriveFR_B)
        self.RR_B = wpilib.CANTalon (constants.DriveRR_B)
        
        self.Drive_A = wpilib.RobotDrive (self.RL_A,
                                          self.FL_A,
                                          self.RR_A,
                                          self.FR_A)

        self.Drive_B = wpilib.RobotDrive (self.RL_B,
                                          self.FL_B,
                                          self.RR_B,
                                          self.FR_B)
										  
        self.Drive_A.setInvertedMotor (2, True)
        self.Drive_A.setInvertedMotor (3, True)
        self.Drive_B.setInvertedMotor (2, True)
        self.Drive_B.setInvertedMotor (3, True)

        self.Drive_A.setExpiration (0.5)
        self.Drive_B.setExpiration (0.5)
        
    def setBrakeEnabled (self, enabled):
        self.FL_A.enableBrakeMode (enabled)
        self.RL_A.enableBrakeMode (enabled)
        self.FR_A.enableBrakeMode (enabled)
        self.RR_A.enableBrakeMode (enabled)
        self.FL_B.enableBrakeMode (enabled)
        self.RL_B.enableBrakeMode (enabled)
        self.FR_B.enableBrakeMode (enabled)
        self.RR_B.enableBrakeMode (enabled)
        
    def setSafetyEnabled (self, enabled):
        self.Drive_A.setSafetyEnabled (enabled)
        self.Drive_B.setSafetyEnabled (enabled)
        
    def move (self, x, y, r):
        x = constants.RemoveDeadband (x)
        y = constants.RemoveDeadband (y)
        r = constants.RemoveDeadband (r)
        
        self.Drive_A.mecanumDrive_Cartesian (x, y, r, 0)
        self.Drive_B.mecanumDrive_Cartesian (x, y, r, 0)
        
    def moveWithJoystick (self, joystick):
        x = 0
        y = 0
        r = 0
        
        angle = joystick.getPOV()
        speed = abs (joystick.getRawAxis (4))

        if angle > -1:
            if (angle == 0 or angle == 45 or angle == 315):
                y = speed
            elif (angle == 135 or angle == 180 or angle == 225):
                y = speed * -1
                
            if (angle == 45 or angle == 90 or angle == 135):
                x = speed
            elif (angle == 225 or angle == 270 or angle == 315):
                x = speed * -1

        else :
            x = joystick.getRawAxis (0)
            y = joystick.getRawAxis (1)
            r = joystick.getRawAxis (4)

        self.move (x, y, r)
        self.setBrakeEnabled (not joystick.getRawButton (1))
