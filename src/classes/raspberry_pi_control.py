import sys
import time
import RPi.GPIO as GPIO


class CarController():

    def __init__(self):
        self.mode = GPIO.getmode()
        #Left motor
        self.in1 = 0
        self.in2 = 0
        self.ena = 0
        #Right motor
        self.in3 = 0
        self.in4 = 0
        self.enb = 0

        GPIO.setMode(GPIO.BCM)
        self.left_motor = GPIO.PWM(self.ena, 1000)
        self.right_motor = GPIO.PWM(self.enb, 1000)
        self.left_motor.start(25)
        self.right_motor.start(25)

    def forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)

    def speedUp(self):
        self.left_motor.ChangeDutyCycle(50)
        self.right_motor.ChangeDutyCycle(50)
    def slowDown(self):
        self.left_motor.ChangeDutyCycle(25)
        self.right_motor.ChangeDutyCycle(25)


    def stop(self):
        GPIO.output(0, GPIO.LOW)

