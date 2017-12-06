#Team 28 Final Demonstration Code

import time
import brickpi3
import grovepi
import math as m
import MasterFunct as PMAD

BP = brickpi3.BrickPi3()
PMAD.startPowerTracking(28)

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) #stop/go button
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.TOUCH) #key code in button
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON) #initialize light sensor
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.CUSTOM, [(BP.SENSOR_CUSTOM.PIN1_ADC)]) #initialize Hall effect Sensor

scrollButton = BP.get_sensor(BP.PORT_4)
goButton = BP.get_sensor(BP.PORT_1)
NXTLight = BP.get_sensor(BP.PORT_2)
hallEffect = BP.get_sensor(BP.PORT_3)
lineSensor = grovepi.digitalRead(8) 

BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))

BP.set_motor_power(BP.PORT_C, 0)
BP.set_motor_power(BP.PORT_B, 0)
lineFinderPin = 8

leftMotorSpeed = 0
rightMotorSpeed = 0

value = 0
speed = 30
destination = 0
hallEffectCounter = 0
distance = 0 #need to assign value

BP.set_motor_power(BP.PORT_B, 0)
BP.set_motor_power(BP.PORT_C, 0)
loopCounter = 0

def lineFollow(): # a function to follow the line
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
        leftMotorSpeed = -65
        rightMotorSpeed = -65*1.12
    BP.set_motor_power(BP.PORT_C, leftMotorSpeed) #update motor speeds
    BP.set_motor_power(BP.PORT_B, rightMotorSpeed)
    return()

def homeLineFollow():
    #a function to bring the robot home from its dropoff zone
    #unsure if needed
    return()

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

def turnLeft():
    NXTLight = BP.get_sensor(BP.PORT_2)
    lineSensor = grovepi.digitalRead(8)
    #Modified version of line following function to choose the left path
    
    if lineSensor == 1 and NXTLight >= 2400:
        leftMotorSpeed = 75
        rightMotorSpeed = -89 * 1.12
        sleep = (0.4)
        print(1)
    elif lineSensor == 1 and NXTLight < 2400:
        leftMotorSpeed = -50
        rightMotorSpeed = 75 * 1.12
        sleep = (0.1)
        print(2)
    elif NXTLight > 2400 and lineSensor == 0:
        leftMotorSpeed = 75
        rightMotorSpeed = -50*1.12
        sleep = 0.1
        print(3)
    else:
        leftMotorSpeed = -30
        rightMotorSpeed = -30*1.12
        sleep = 0.1
    BP.set_motor_power(BP.PORT_C, leftMotorSpeed) #update motor speeds
    BP.set_motor_power(BP.PORT_B, rightMotorSpeed)
    #time.sleep(sleep)
    return()

def readHallEffect():
    global hallEffect
    try:
        ref5v = (4095.0 / BP.get_voltage_5v())
        hallEffectRead = (hallEffect/ref5v)
        time.sleep(0.2)
    except brickpi3.SensorError as error:
        print(error)
    if hallEffectRead > 2.6:
        read = 1
    else:
        read = 0           
    #read hall effect and assign a boolean of yes/no
    #may need to include data filtration
    return(read)

def goStraight():
    lineSensor = grovepi.digitalRead(8)
    #a function to ignore the left line and go straight to pass a dropoff site
    if lineSensor == 1:
        leftMotorSpeed = -15
        rightMotorSpeed = -80*1.12
    else:
        leftMotorSpeed = -80
        rightMotorSpeed = -15 * 1.12

    BP.set_motor_power(BP.PORT_B, leftMotorSpeed) #update motor speeds
    BP.set_motor_power(BP.PORT_C, rightMotorSpeed)
    #time.sleep(0.1)
    return()

def lineFindHill():
    if lineSensor == 1:
        leftMotorSpeed = 75
        rightMotorSpeed = -50 * 1.12
    elif(NXTLight > 1900):
        leftMotorSpeed = -50
        rightMotorSpeed = 75*1.12
    else:
        leftMotorSpeed = 89
        rightMotorSpeed = 89*1.12

    BP.set_motor_power(BP.PORT_C, leftMotorSpeed) #update motor speeds
    BP.set_motor_power(BP.PORT_B, rightMotorSpeed)
    return()

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

home = False
gyroRead = 0

while not value:#see about indication
    try:
       value = goButton
       if scrollButton == 1:
           desination = destination + 1
           x = True
           while x:
               if scrollButton == 0:
                   x = False
                   break
       if destination >= 4:
            destination = 0
    except brickpi3.SensorError:
       value = 0

while value:
    if loopCounter < 1:
        BP.set_motor_power(BP.PORT_B, 15) #update motor speeds
        BP.set_motor_power(BP.PORT_C, 15*1.12)
        loopCounter = loopCounter + 1
        timeInitial = time.time()
    else:
#        gyroRead = checkGyro()
#        while gyroRead == 1:
#            lineFindHill()
#            gyroRead = checkGyro()
#
        checkPMAD()
        lineFollow()
        hallEffectRead = readHallEffect()
        if hallEffectRead == 1 and (time.time()-timeInitial) > 3:
            hallEffectCounter = hallEffectCounter + 1
            z = True
            while z:
                hallEffectRead = readHallEffect()
                if hallEffectRead == 0:
                    z = False
                    break
        if destination == 1 and hallEffectCounter == 1:
            #take the left path if we want site Alpha
            x = True
            while x:
                checkPMAD()
                turnLeft()
                if hallEffectCounter == 2:
                    x = False
                    dropOff()
                    home = True
        elif (destination == 2 and hallEffectCounter == 1) or\
        (destination == 3 and hallEffectCounter == 1):
            #go straight if we want site Beta or Gamma and we see beacon 1
            x = True
            while(x):
                checkPMAD()
                goStraight()
                if destination == 2 and hallEffectCounter == 2:
                    #turn left at line if we want site Beta and see a
                    #second beacon
                    x = True
                    while(x):
                        checkPMAD()
                        turnLeft()
                        if hallEffectCounter == 3:
                            dropOff()
                            home = True
                            x = False
                            break
                elif destination == 3 and hallEffectCounter == 2:
                    #go straight if we want site Gamma and see a second 
                    #beacon
                    x = True
                    while(x):
                        checkPMAD()
                        goStraight()
                        if destination == 3 and hallEffectCounter == 3:
                            #turn left if we see a third beacon and have
                            #selected site Gamma
                            y = True
                            while(y):
                                checkPMAD()
                                turnLeft()
                                if hallEffectCounter == 4:
                                    dropOff()
                                    home = True
                                    y = False
                                    x = False
                                    break
        while(home):
            checkPMAD()
            lineFollow() #home line follow?
            hallEffectRead = readHallEffect()
            if hallEffectRead == 1:
                BP.set_motor_power(BP.PORT_B, 0) #stop at beacon
                BP.set_motor_power(BP.PORT_C, 0)
                hallEffectCounter = 0
                value = False
                break                        
    time.sleep(0.001)