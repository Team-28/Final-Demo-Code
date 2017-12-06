
import brickpi3

BP = brickpi3.BrickPi3()

BP.set_motor_power(BP.PORT_A, 0) 
BP.set_motor_power(BP.PORT_B, 0)
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
value = 0
while not value:
    try:
       value = BP.get_sensor(BP.PORT_3)
    except brickpi3.SensorError:
       value = 0
    BP.set_motor_power(BP.PORT_A, -30) 
    BP.set_motor_power(BP.PORT_B, -30) 
    loopCounter = 0
while value:
    BP.set_motor_power(BP.PORT_A, 0) 
    BP.set_motor_power(BP.PORT_B, 0)
    