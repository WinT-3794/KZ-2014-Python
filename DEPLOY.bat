@echo off
title KZ14-Python Deployment
echo Robot Deployment Program
echo Copyright (c) 2014-2016 WinT 3794 [http://wint3794.org]
echo.
echo ROBOT    : Kooz 2014
echo LANGUAGE : Python [http://robotpy.readthedocs.org/]
echo WIRING   : CAN bus
echo.
echo PLEASE CLEAR THE OPERATION ZONE BEFORE PROCEEDING
echo.
pause
cls
py src/robot.py deploy --builtin
pause