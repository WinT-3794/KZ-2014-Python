#!/usr/bin/env python3

'''
' Copyright (c) 2015 WinT 3794 <http://wint3794.org>
'
' Permission is hereby granted, free of charge, to any person obtaining a copy
' of this software and associated documentation files (the "Software"), to deal
' in the Software without restriction, including without limitation the rights
' to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
' copies of the Software, and to permit persons to whom the Software is
' furnished to do so, subject to the following conditions:
'
' The above copyright notice and this permission notice shall be included in
' all copies or substantial portions of the Software.
'
' THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
' IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
' FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
' AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
' LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
' OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
' THE SOFTWARE.
'''

import wpilib

# Define the maximum operator outputs
AXIS_POWER          = 0.85
BUTTON_POWER        = 0.70

# Define CAN Controller IDs
CAN_CIM_FL          = 0x04
CAN_CIM_RL          = 0x01
CAN_CIM_FR          = 0x05
CAN_CIM_RR          = 0x0A
CAN_MINI_CIM_FL     = 0x03
CAN_MINI_CIM_RL     = 0x02
CAN_MINI_CIM_FR     = 0x06
CAN_MINI_CIM_RR     = 0x09
CAN_SHOOTER_A       = 0x07
CAN_SHOOTER_B       = 0x08

# Define PWM Controller IDs
PWM_ANDYMARK_LIFTER = 0X00

class Kooz2014 (wpilib.IterativeRobot):
    def initializeControllers (self):
        # CIM Drive motors
        self.CIM_FL = wpilib.CANTalon (CAN_CIM_FL)
        self.CIM_RL = wpilib.CANTalon (CAN_CIM_RL)
        self.CIM_FR = wpilib.CANTalon (CAN_CIM_FR)
        self.CIM_RR = wpilib.CANTalon (CAN_CIM_RR)

        # MiniCIM Drive motors
        self.MiniCIM_FL = wpilib.CANTalon (CAN_MINI_CIM_FL)
        self.MiniCIM_RL = wpilib.CANTalon (CAN_MINI_CIM_RL)
        self.MiniCIM_FR = wpilib.CANTalon (CAN_MINI_CIM_FR)
        self.MiniCIM_RR = wpilib.CANTalon (CAN_MINI_CIM_RR)

        # Shooter motors
        self.Shooter_A = wpilib.CANTalon (CAN_SHOOTER_A)
        self.Shooter_B = wpilib.CANTalon (CAN_SHOOTER_B)

        # Lifter motors
        self.Lifter = wpilib.VictorSP (PWM_ANDYMARK_LIFTER)

        # Configure the brake mode
        self.setBrakeEnabled (True)
        self.Shooter_A.enableBrakeMode (False)
        self.Shooter_B.enableBrakeMode (False)

    def initializeDriveSystems (self):
        self.CIM_Drive = wpilib.RobotDrive (1, 2, 3, 4)
        self.MiniCIM_Drive = wpilib.RobotDrive (5, 6, 7, 8)

    def setControlEnabled (self, enabled):
        # Enable the Talons
        if (enabled):
            self.CIM_FL.enableControl()
            self.CIM_RL.enableControl()
            self.CIM_FR.enableControl()
            self.CIM_RR.enableControl()
            self.Shooter_A.enableControl()
            self.Shooter_B.enableControl()
            self.MiniCIM_FL.enableControl()
            self.MiniCIM_RL.enableControl()
            self.MiniCIM_FR.enableControl()
            self.MiniCIM_RR.enableControl()

        else:
            self.CIM_FL.disableControl()
            self.CIM_RL.disableControl()
            self.CIM_FR.disableControl()
            self.CIM_RR.disableControl()
            self.Shooter_A.disableControl()
            self.Shooter_B.disableControl()
            self.MiniCIM_FL.disableControl()
            self.MiniCIM_RL.disableControl()
            self.MiniCIM_FR.disableControl()
            self.MiniCIM_RR.disableControl()

    def setBrakeEnabled (self, enabled):
        self.CIM_FL.enableBrakeMode (enabled)
        self.CIM_RL.enableBrakeMode (enabled)
        self.CIM_FR.enableBrakeMode (enabled)
        self.CIM_RR.enableBrakeMode (enabled)
        self.MiniCIM_FL.enableBrakeMode (enabled)
        self.MiniCIM_RL.enableBrakeMode (enabled)
        self.MiniCIM_FR.enableBrakeMode (enabled)
        self.MiniCIM_RR.enableBrakeMode (enabled)

    def setSafetyEnabled (self, enabled):
        # Drive systems
        self.CIM_Drive.setSafetyEnabled (enabled)
        self.MiniCIM_Drive.setSafetyEnabled (enabled)

        # Shooter motors
        self.Shooter_A.setSafetyEnabled (enabled)
        self.Shooter_B.setSafetyEnabled (enabled)

        # Lifter motor
        self.Lifter.setSafetyEnabled (enabled)
        
    def moveDriveSystem (self, x, y, r):
        self.CIM_Drive.mecanumDrive_Cartesian (x, y, r, 0)
        self.MiniCIM_Drive.mecanumDrive_Cartesian (x, y, r, 0)

    def moveShooters (self, value):
        self.Shooter_A.set (value)
        self.Shooter_B.set (value)

    def moveLifter (self, value):
        self.Lifter.set (value)
        
    def moveDriveWithJoystick (self, joystick):
        # Press A to surf, watch for people and windows!
        if (joystick.getRawButton (1)):
            self.setBrakeEnabled (False)

        # Press B to re-enable CAN controllers if they stop working
        if (joystick.getRawButton (2)):
            self.setControlEnabled (True)

        # Move the chassis with the joystick axes
        self.moveDriveSystem (joystick.getX() * AXIS_POWER,
                              joystick.getY() * AXIS_POWER,
                              joystick.getZ() * AXIS_POWER)

    def moveLifterWithJoystick (self, joystick):
        # Press the left bumper to lift the ball
        if (joystick.getRawButton (5)):
            self.moveLifter (BUTTON_POWER)

        # Press the right bumper to !lift the ball
        if (joystick.getRawButton (6)):
            self.moveLifter (BUTTON_POWER)

    def moveShooterWithJoystick (self, joystick):
        # Get joystick trigger values
        left = joystick.getRawAxis (2)
        right = joystick.getRawAxis (3)

        # Only proceed if trigger values are different
        if (left == right):
            return
        
        # Allign the shooter (move upwards)
        if (left > right):
            self.moveShooters (left)

        # Shoot the ball (move downwards)
        elif (right < left):
            self.moveShooters (right * -1)

    def updateConfiguration (self):
        # Get autonomous values from SmartDashboard
        self.Auto_DriveTime = wpilib.SmartDashboard.getDouble ("Drive Time (seconds)", 4)
        self.Auto_ShooterTime = wpilib.SmartDashboard.getDouble ("Shooter Time (seconds)", 2)
        self.Auto_DriveOutput = wpilib.SmartDashboard.getDouble ("Motor Output (autonomous)", 0.6)
        self.Auto_GoBackwards = wpilib.SmartDashboard.getBoolean ("Drive Backwards (autonomous)", False)

        # Get single operator configuration from SmartDashboard
        self.SingleOperator = wpilib.SmartDashboard.getBoolean ("Single Operator", False)
        
    def robotInit (self):
        # Initialize all robot systems
        self.initializeControllers()
        self.initializeDriveSystems()

        # Initialize the joysticks
        self.Joystick_Primary = wpilib.Joystick (0)
        self.Joystick_Secondary = wpilib.Joystick (1)
        self.Joystick_Volatile = self.Joystick_Secondary

        # Get SmartDashboard values
        self.updateConfiguration()

    def teleopInit (self):
        # Get SmartDashboard values and enable CAN controllers
        self.updateConfiguration()
        self.setControlEnabled (True)

        # Decide if we should enable the single operator feature
        if (self.SingleOperator):
            self.Joystick_Volatile = self.Joystick_Primary
        else:
            self.Joystick_Volatile = self.Joystick_Secondary

        # Make sure that we don't obtain a flying saucer
        self.setSafetyEnabled (True)

    def disabledInit (self):
        # Make sure safety is enabled and disable Talons
        self.setSafetyEnabled (True)
        self.setControlEnabled (False)

    def autonomousInit (self):
        # Get SmartDashboard values again and enable CAN controllers
        self.updateConfiguration()
        self.setControlEnabled (True)
        
    def teleopPeriodic (self):
        # Move the drive system with the first joystick
        self.moveDriveWithJoystick (self.Joystick_Primary)
        
        # Based on the values obtained from the SmartDashboard,
        # we can move the shooter and lifter with any of the two joysticks
        self.moveLifterWithJoystick (self.Joystick_Volatile)
        self.moveShooterWithJoystick (self.Joystick_Volatile)

    def autonomousPeriodic (self):
        return

if (__name__ == "__main__"):
    wpilib.run (Kooz2014)
