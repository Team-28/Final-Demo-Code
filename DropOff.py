#Team 28 Final Demo code-- cargo dropoff from beacon

import time
import brickpi3
import grovepi
import math as m
import MasterFunct as PMAD
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3()
#PMAD.startPowerTracking(28)

BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) #stop/go button
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH) #key code in button
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON) #initialize light sensor
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.CUSTOM, [(BP.SENSOR_CUSTOM.PIN1_ADC)]) #initialize Hall effect Sensor

time.sleep(1)

scrollButton = BP.get_sensor(BP.PORT_4)
goButton = BP.get_sensor(BP.PORT_1)
NXTLight = BP.get_sensor(BP.PORT_2)
hallEffect = BP.get_sensor(BP.PORT_3)
lineSensor = grovepi.digitalRead(8) 

distance = 360 #need to assign value

BP.set_motor_power(BP.PORT_B, 0)
BP.set_motor_power(BP.PORT_C, 0)
def dropOff():
    #drive past beacon then dropoff cargo
    #18.5cm
    timeInitial = time.time()
    x = True
    while(x):
        line = BP.get_sensor(BP.PORT_2)
        lineSensor = grovepi.digitalRead(8)     

        if lineSensor == 1:
            leftMotorSpeed = -50
            rightMotorSpeed = 75 * 1.12
            print(lineSensor)
        elif(line > 2400):
            leftMotorSpeed = 75
            rightMotorSpeed = -50*1.12
            print(line)
        else:
            leftMotorSpeed = -30
            rightMotorSpeed = -30*1.12
        if time.time() - timeInitial >= 2:
            x = False
            break
        BP.set_motor_power(BP.PORT_C, leftMotorSpeed) #update motor speeds
        BP.set_motor_power(BP.PORT_B, rightMotorSpeed)
    
    BP.set_motor_power(BP.PORT_C, 0) 
    BP.set_motor_power(BP.PORT_B, 0)
    aPos =  BP.get_motor_encoder(BP.PORT_A)
    dPos = BP.get_motor_encoder(BP.PORT_D)
    dSet = dPos - 100
    BP.set_motor_position(BP.PORT_A, (aPos + -600))#check sign
    BP.set_motor_position(BP.PORT_D, (dSet))#check sign
    time.sleep(1)
    timeInitial2 = time.time()
    y = True
    while(y):
        line = BP.get_sensor(BP.PORT_2)
        lineSensor = grovepi.digitalRead(8)     

        if lineSensor == 1:
            leftMotorSpeed = -50
            rightMotorSpeed = 75 * 1.12
            print(lineSensor)
        elif(line > 2400):
            leftMotorSpeed = 75
            rightMotorSpeed = -50*1.12
            print(line)
        else:
            leftMotorSpeed = -30
            rightMotorSpeed = -30*1.12
        if time.time() - timeInitial2 >= 2:
            BP.set_motor_power(BP.PORT_C, 0) 
            BP.set_motor_power(BP.PORT_B, 0)
            y = False
            break
        BP.set_motor_power(BP.PORT_C, leftMotorSpeed) #update motor speeds
        BP.set_motor_power(BP.PORT_B, rightMotorSpeed)
        
    BP.set_motor_position(BP.PORT_D, (dPos))#check sign
    BP.set_motor_power(BP.PORT_A, BP.MOTOR_FLOAT)
    return()

dropOff()


if goButton == 1:
    BP.set_motor_power(BP.PORT_B + BP.PORT_C, BP.MOTOR_FLOAT)
