import sys
import time
import RPi.GPIO as GPIO
from .. import Constants


class CarController():

    def __init__(self):
        self.mode = GPIO.getmode()

        # Left motor
        self.in1 = Constants.IN1_PORT
        self.in2 = Constants.IN2_PORT
        self.ena = Constants.ENA_PORT


        # Right motor
        self.in3 = Constants.IN3_PORT
        self.in4 = Constants.IN4_PORT
        self.enb = Constants.ENB_PORT

        GPIO.setMode(GPIO.BCM)
        self.left_motor = GPIO.PWM(self.ena, 1000)
        self.right_motor = GPIO.PWM(self.enb, 1000)

        # Initial Duty Cycle - 25%
        self.left_motor.start(25)
        self.right_motor.start(25)

        # Proportional constant
        self.kP = Constants.kP

    def set_output(self,left_speed,right_speed):
        self.set_left(left_speed)
        self.set_right(right_speed)

    def set_left(self, output):
        if output < 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        else:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)

        # change from value between -1 - 1 to 0 - 100
        output = abs(output * 100)
        self.left_motor.ChangeDutyCycle(output)

    def set_right(self, output):
        if output < 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        else:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)

        output = abs(output * 100)
        self.right_motor.ChangeDutyCycle(output)


class SensorData():

    def __init__(self):
        GPIO.setMode(GPIO.BCM)
        # Trigger and Echo Pins
        self.trigger = Constants.TRIGGER_PORT
        self.echo = Constants.ECHO_PORT

        # Setup trigger and echo ports
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def distance(self):

        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        start_time = time.time()
        end_time = time.time()

        while GPIO.input(self.echo) == 0:
            start_time = time.time()

        while GPIO.input(self.echo) == 1:
            end_time = time.time()

        elapsed = start_time - end_time
        # multiply time * speed of sound
        # divide by 2 (sound goes there and bounces back)
        distance = (elapsed * 34300) / 2

        return distance
