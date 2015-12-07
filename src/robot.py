#!/usr/bin/env python3

# Define the maximum operator outputs
AXIS_POWER          = 0.85
BUTTON_POWER        = 0.70

# Define CAN Controller IDs
CAN_CIM_FL          = 4
CAN_CIM_RL          = 1
CAN_CIM_FR          = 5
CAN_CIM_RR          = 10
CAN_MINI_CIM_FL     = 3
CAN_MINI_CIM_RL     = 2
CAN_MINI_CIM_FR     = 6
CAN_MINI_CIM_RR     = 9
CAN_SHOOTER_A       = 7
CAN_SHOOTER_B       = 8

# Define PWM Controller IDs
PWM_ANDYMARK_LIFTER = 0

import wpilib

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

    def setBrakeEnabled (self, brake):
        self.CIM_FL.enableBrakeMode (brake)
        self.CIM_RL.enableBrakeMode (brake)
        self.CIM_FR.enableBrakeMode (brake)
        self.CIM_RR.enableBrakeMode (brake)
        self.MiniCIM_FL.enableBrakeMode (brake)
        self.MiniCIM_RL.enableBrakeMode (brake)
        self.MiniCIM_FR.enableBrakeMode (brake)
        self.MiniCIM_RR.enableBrakeMode (brake)

    def setSafetyEnabled (self, enabled):
        self.Lifter.setSafetyEnabled (enabled)
        self.Shooter_A.setSafetyEnabled (enabled)
        self.Shooter_B.setSafetyEnabled (enabled)
        self.CIM_Drive.setSafetyEnabled (enabled)
        self.MiniCIM_Drive.setSafetyEnabled (enabled)
        
    def moveDriveSystem (self, x, y, r):
        self.CIM_Drive.mecanumDrive_Cartesian (x, y, r, 0)
        self.MiniCIM_Drive.mecanumDrive_Cartesian (x, y, r, 0)

    def moveShooters (self, value):
        self.Shooter_A.set (value)
        self.Shooter_B.set (value)

    def moveLifter (self, value):
        self.Lifter.set (value)
        
    def moveDriveWithJoystick (self, joystick):
        # Press A to coast, watch for people and windows!
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

        # Press the right bumper to release the ball
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

    def refreshSettings (self):
        self.SingleOperator = wpilib.SmartDashboard.getBoolean ("Single Operator", False)
        self.Auto_DriveTime = wpilib.SmartDashboard.getDouble ("Drive Time (seconds)", 4)
        self.Auto_ShooterTime = wpilib.SmartDashboard.getDouble ("Shooter Time (seconds)", 2)
        self.Auto_DriveOutput = wpilib.SmartDashboard.getDouble ("Motor Output (autonomous)", 0.6)
        self.Auto_GoBackwards = wpilib.SmartDashboard.getBoolean ("Drive Backwards (autonomous)", False)
        
    def robotInit (self):
        self.refreshSettings()
        self.initializeControllers()
        self.initializeDriveSystems()

        self.Joystick_Primary = wpilib.Joystick (0)
        self.Joystick_Secondary = wpilib.Joystick (1)
        self.Joystick_Volatile = self.Joystick_Secondary

    def teleopInit (self):
        self.refreshSettings()
        self.setSafetyEnabled (True)
        self.setControlEnabled (True)

        if (self.SingleOperator):
            self.Joystick_Volatile = self.Joystick_Primary
        else:
            self.Joystick_Volatile = self.Joystick_Secondary

    def disabledInit (self):
        self.setSafetyEnabled (True)
        self.setControlEnabled (False)

    def autonomousInit (self):
        self.refreshSettings()
        self.setControlEnabled (True)
        
    def teleopPeriodic (self):
        self.moveDriveWithJoystick (self.Joystick_Primary)
        self.moveLifterWithJoystick (self.Joystick_Volatile)
        self.moveShooterWithJoystick (self.Joystick_Volatile)

    def autonomousPeriodic (self):
        return

if (__name__ == "__main__"):
    wpilib.run (Kooz2014)
