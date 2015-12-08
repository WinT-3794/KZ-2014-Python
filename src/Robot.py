#-----------------------------------------------------------------------------#
# Copyright (c) WinT 3794 <http://wint3794.org                                #
# Open Source Software - may be modified and shared by anyone.                #
# The code must be accompanied by the DBAD license file in the root directory #
# of the project.                                                             #
#-----------------------------------------------------------------------------#

import math
import wpilib

# Define the maximum operator outputs
OP_AXIS_POWER          = 0.85
OP_BUTTON_POWER        = 0.75

# Define dead-band values
DB_MIN_VALUE           = 0.15

# Define CAN Controller IDs
ID_CAN_CIM_FL          = 4
ID_CAN_CIM_RL          = 1
ID_CAN_CIM_FR          = 5
ID_CAN_CIM_RR          = 10
ID_CAN_MCIM_FL         = 3
ID_CAN_MCIM_RL         = 2
ID_CAN_MCIM_FR         = 6
ID_CAN_MCIM_RR         = 9
ID_CAN_SHOOTER_A       = 7
ID_CAN_SHOOTER_B       = 8

# Define PWM Controller IDs
ID_PWM_ANDYMARK_LIFTER = 0

# Define the SmartDashboard keys
SD_DEADBAND            = "Deadband Limit"
SD_DRIVE_TIME          = "Autonomous Drive Time (seconds)"
SD_SHOOTER_TIME        = "Autonomous Shooter Time (seconds"
SD_BACKWARDS           = "Drive Backwards during Autonomous"
SD_ONE_JS              = "Control everything with one joystick"

class Kooz2014 (wpilib.IterativeRobot):
    def initializeControllers (self):
        # CIM Drive motors
        self.CIM_FL = wpilib.CANTalon (ID_CAN_CIM_FL)
        self.CIM_RL = wpilib.CANTalon (ID_CAN_CIM_RL)
        self.CIM_FR = wpilib.CANTalon (ID_CAN_CIM_FR)
        self.CIM_RR = wpilib.CANTalon (ID_CAN_CIM_RR)

        # MiniCIM Drive motors
        self.mCIM_FL = wpilib.CANTalon (ID_CAN_MCIM_FL)
        self.mCIM_RL = wpilib.CANTalon (ID_CAN_MCIM_RL)
        self.mCIM_FR = wpilib.CANTalon (ID_CAN_MCIM_FR)
        self.mCIM_RR = wpilib.CANTalon (ID_CAN_MCIM_RR)

        # Shooter motors
        self.Shooter_A = wpilib.CANTalon (ID_CAN_SHOOTER_A)
        self.Shooter_B = wpilib.CANTalon (ID_CAN_SHOOTER_B)

        # Lifter motors
        self.Lifter = wpilib.VictorSP (ID_PWM_ANDYMARK_LIFTER)

    def initializeDriveSystems (self):
        # Initialize CIM drive
        self.CIM_Drive  = wpilib.RobotDrive (self.CIM_RL,
                                             self.CIM_FL,
                                             self.CIM_RR,
                                             self.CIM_FR)

        # Initialize Mini CIM drive
        self.mCIM_Drive = wpilib.RobotDrive (self.mCIM_RL,
                                             self.mCIM_FL,
                                             self.mCIM_RR,
                                             self.mCIM_FR)

        # Configure the drive systems
        self.CIM_Drive.setExpiration (0.5)
        self.mCIM_Drive.setExpiration (0.5)

    def setBrakeEnabled (self, brake):
        # Update brake mode of CIM motors
        self.CIM_FL.enableBrakeMode (brake)
        self.CIM_RL.enableBrakeMode (brake)
        self.CIM_FR.enableBrakeMode (brake)
        self.CIM_RR.enableBrakeMode (brake)

        # Update brake mode of Mini CIM motors
        self.mCIM_FL.enableBrakeMode (brake)
        self.mCIM_RL.enableBrakeMode (brake)
        self.mCIM_FR.enableBrakeMode (brake)
        self.mCIM_RR.enableBrakeMode (brake)

    def setSafetyEnabled (self, enabled):
        # Update lifter settings
        self.Lifter.setSafetyEnabled (enabled)

        # Update shooter settings
        self.Shooter_A.setSafetyEnabled (enabled)
        self.Shooter_B.setSafetyEnabled (enabled)

        # Update CIM drive settings
        self.CIM_FL.setSafetyEnabled (enabled)
        self.CIM_RL.setSafetyEnabled (enabled)
        self.CIM_FR.setSafetyEnabled (enabled)
        self.CIM_RR.setSafetyEnabled (enabled)

        # Update Mini CIM drive settings
        self.mCIM_FL.setSafetyEnabled (enabled)
        self.mCIM_RL.setSafetyEnabled (enabled)
        self.mCIM_FR.setSafetyEnabled (enabled)
        self.mCIM_RR.setSafetyEnabled (enabled)

    def removeDeadband (self, value):
        # The movement is considered involuntary
        if abs (value) < self.DeadbandLimit:
            return value

        # Value is greater than the deadband limit
        else:
            return value

    def moveDriveSystem (self, x, y, r):
        # Remove deadband from input values
        x = self.removeDeadband (x)
        y = self.removeDeadband (y)
        r = self.removeDeadband (r)

        # Update the drive motors
        self.CIM_Drive.mecanumDrive_Cartesian  (x, y, r, 0)
        self.mCIM_Drive.mecanumDrive_Cartesian (x, y, r, 0)

    def moveShooters (self, value):
        # Remove deadband from input values
        value = self.removeDeadband (value)

        # Update the shooter motors
        self.Shooter_A.set (value)
        self.Shooter_B.set (value)

    def moveLifter (self, value):
        self.Lifter.set (self.removeDeadband (value))

    def moveDriveWithJoystick (self, joystick):
        # Press A to coast, watch for people and windows!
        self.setBrakeEnabled (not joystick.getRawButton (1))

        # By default, the robot will not move
        x = 0
        y = 0
        z = 0

        # Use the joystick hats/POVs to move the chassis,
        # the POV will give us an angle in degrees (0-360), we can use
        # that value to decide where and how to move our robot
        angle = joystick.getPOV()
        if angle > -1:
            # The robot will move forward
            if (angle == 0 or angle == 45 or angle == 315):
                y = OP_BUTTON_POWER

            # The robot will move backward
            if (angle == 135 or angle == 180 or angle == 225):
                y = OP_BUTTON_POWER * -1

            # The robot will move rightward
            if (angle == 45 or angle == 90 or angle == 135):
                x = OP_BUTTON_POWER

            # The robot will move leftward
            if (angle == 225 or angle == 270 or angle == 315):
                x = OP_BUTTON_POWER * -1

        # Move the chassis with the joystick axes, we switch
        # the Y and Z to correct robot heading on rough terrain
        # (such as school presentations) more easily.
        else :
            x = joystick.getX() * OP_AXIS_POWER
            y = joystick.getZ() * OP_AXIS_POWER
            z = joystick.getY() * OP_AXIS_POWER

        # Finally, move the drive system with the obtained values
        self.moveDriveSystem (x, y, z)

    def moveLifterWithJoystick (self, joystick):
        # Press the left bumper to lift the ball
        if joystick.getRawButton (5):
            self.moveLifter (OP_BUTTON_POWER)

        # Press the right bumper to release the ball
        if joystick.getRawButton (6):
            self.moveLifter (OP_BUTTON_POWER)

    def moveShooterWithJoystick (self, joystick):
        # Get joystick trigger values
        value = 0
        left = joystick.getRawAxis (2)
        right = joystick.getRawAxis (3)

        # Decide in which direction we should shoot
        if left > right:
            value = left
        elif right > left:
            value = right * -1

        # Finally, move the shooter motors
        self.moveShooters (value)

    def refreshSettings (self):
        # Get autonomous settings from SmartDashboard
        self.DriveTime = wpilib.SmartDashboard.getDouble (SD_DRIVE_TIME, 4)
        self.ShooterTime = wpilib.SmartDashboard.getDouble (SD_SHOOTER_TIME, 2)
        self.Backwards = wpilib.SmartDashboard.getBoolean (SD_BACKWARDS, False)

        # Get operator settings
        self.SingleDriver = wpilib.SmartDashboard.getBoolean (SD_ONE_JS, False)
        self.DeadbandLimit = wpilib.SmartDashboard.getDouble (SD_DEADBAND, 0.1)

    def robotInit (self):
        # Initialize motors and drive system
        self.initializeControllers()
        self.initializeDriveSystems()

        # Shooter should brake, it may be to lose if we let it coast
        self.Shooter_A.enableBrakeMode (True)
        self.Shooter_B.enableBrakeMode (True)

        # Initialize the joysticks
        self.Joystick_Primary = wpilib.Joystick (0)
        self.Joystick_Secondary = wpilib.Joystick (1)
        self.Joystick_Volatile = self.Joystick_Secondary

        # Get settings from SmartDashboard
        self.refreshSettings()

    def teleopInit (self):
        self.refreshSettings()
        self.setBrakeEnabled (True)
        self.setSafetyEnabled (True)

        # Decide if we should use one joystick or both
        if self.SingleDriver:
            self.Joystick_Volatile = self.Joystick_Primary
        else:
            self.Joystick_Volatile = self.Joystick_Secondary

    def disabledInit (self):
        self.setBrakeEnabled (True)
        self.setSafetyEnabled (True)

    def autonomousInit (self):
        self.refreshSettings()
        self.setBrakeEnabled (True)
        self.visitedAutonomous = False

    def teleopPeriodic (self):
        # The drive motors are always moved with primary joystick
        self.moveDriveWithJoystick (self.Joystick_Primary)

        # The shooter and lifter can be moved with both joysticks
        self.moveLifterWithJoystick (self.Joystick_Volatile)
        self.moveShooterWithJoystick (self.Joystick_Volatile)

    def autonomousPeriodic (self):
        # This ensures that the code will only run once during the Auto period
        if not self.visitedAutonomous:
            self.visitedAutonomous = True

            # Disable safety features so that we move motors with timers
            self.setSafetyEnabled (False)

            # Move the drive system
            if not self.Backwards:
                self.moveDriveSystem (0, OP_BUTTON_POWER, 0)
            else:
                self.moveDriveSystem (0, OP_BUTTON_POWER * -1, 0)

            # Wait some time and stop the drive system
            wpilib.Timer.delay (self.DriveTime * 1000)
            self.moveDriveSystem (0, 0, 0)

            # Move the shooter system
            self.moveShooters (self.MotorOutput)

            # Wait some time and stop the shooters
            wpilib.Timer.delay (self.ShooterTime * 1000)
            self.moveShooters (0)

            # Enable the safety features again
            self.setSafetyEnabled (True)

        return

if (__name__ == "__main__"):
    wpilib.run (Kooz2014)
