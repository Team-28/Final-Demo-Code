#Team 28 Line Following Code

import time
import brickpi3
import grovepi
import math as m
import MasterFunct as PMAD

PMAD.startPowerTracking(28)
BP = brickpi3.BrickPi3()


BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
NXTLightSensorThreshold = 2000# define value for black vs white
lineFinderPin = 8

leftMotorSpeed = 0
rightMotorSpeed = 0



print("Press button to begin")

value = 0
speed = 30

BP.set_motor_power(BP.PORT_B, 0)
BP.set_motor_power(BP.PORT_C, 0)

def checkPMAD():
    power = PMAD.getPowerStored()
    if power.isDigit() == True and power < 10:
        #sleep robot to recharge then go
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)
        time.sleep(10)
        BP.set_motor_power(BP.PORT_B, 15)
        BP.set_motor_power(BP.PORT_C, 15*1.12)
    return()

def lineFollow(): # a function to follow the line
    NXTLight = BP.get_sensor(BP.PORT_2)
    lineSensor = grovepi.digitalRead(8)
    if lineSensor == 1:
        leftMotorSpeed = -300
        rightMotorSpeed = 460 * 1.12
    elif(NXTLight > 2400):
        leftMotorSpeed = 460
        rightMotorSpeed = -300*1.12
    else:
        leftMotorSpeed = -360
        rightMotorSpeed = -360*1.12

    BP.set_motor_dps(BP.PORT_C, leftMotorSpeed) #update motor speeds
    BP.set_motor_dps(BP.PORT_B, rightMotorSpeed)
    return()
value = 0
while not value:
    value = BP.get_sensor(BP.PORT_1)
    lineFollow()
    checkPMAD()
while value:
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
