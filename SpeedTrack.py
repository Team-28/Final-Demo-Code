#Team 28 Speed regulation Code

import time     
import brickpi3
import math as m
 
wheelDiameter = 8.2
BP = brickpi3.BrickPi3()
targetSpeed = 5 #input rate in cm/s

encoderSpeed = targetSpeed*360/(m.pi*wheelDiameter)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

value = 0

while not value:
    try:
       value = BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError:
       value = 0
    BP.set_motor_limits(BP.PORT_B, 100)
    BP.set_motor_limits(BP.PORT_C, 100)
    while True:
        BP.set_motor_dps(BP.PORT_B, targetSpeed)
        BP.set_motor_dps(BP.PORT_C, targetSpeed)
        
        if ((((BP.get_motor_encoder(BP.PORT_B)*wheelDiameter*m.pi/360)**2)**0.5) > 250) or \
        ((((BP.get_motor_encoder(BP.PORT_C)*wheelDiameter*m.pi/360)**2)**0.5) > 250):
            BP.set_motor_power(BP.PORT_B, 0)
            BP.set_motor_power(BP.PORT_C, 0)
            value = False
            break
        time.sleep(0.02)
