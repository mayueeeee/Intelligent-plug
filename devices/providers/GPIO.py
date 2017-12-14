import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Switch_1
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Switch_2
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Switch_Change_screen
GPIO.setup(19,GPIO.OUT) # Relay CH1
GPIO.setup(26,GPIO.OUT) # Relay CH2
GPIO.setup(21,GPIO.OUT) # LED CH1
GPIO.setup(20,GPIO.OUT) # LED CH1

switch_1 = GPIO.input(5)
switch_2 = GPIO.input(6)
switch_cs = GPIO.input(13)


def setSwitch(id,state):
    if id is 1:
        GPIO.output(19,state)
        GPIO.output(21,state)
    elif id is 2:
        GPIO.output(26,state)
        GPIO.output(20,state)

def readSwitch1():
    return GPIO.input(5)

def readSwitch2():
    return GPIO.input(6)
