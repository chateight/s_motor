#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#    Stepper Motor Test
#
# A simple script to control
# a stepper motor.
#
# Author : Matt Hawkins
# Date   : 28/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
# *** using this source for my application(2021/11) ***
#
# Import required libraries
import sys
import time
import RPi.GPIO as GPIO
import subprocess

class motor_drive:
# Define GPIO signals to drive s_motor
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
  StepPins = [17,22,23,24]
# shutdown and rotate direction pins
  SHUTDOWN = 16   
  r_left = 25
  r_right = 26

      
  def __init__(self):
      # Use BCM GPIO references
      # instead of physical pin numbers
      GPIO.setmode(GPIO.BCM)

      # Set all pins as output
      for pin in self.StepPins:
          print("Setup pins")
          GPIO.setup(pin,GPIO.OUT)
          GPIO.output(pin, False)
      # shutdown & direction DIO definition
      GPIO.setup(self.SHUTDOWN, GPIO.IN, GPIO.PUD_UP) 
      GPIO.setup(self.r_left, GPIO.IN, GPIO.PUD_UP) 
      GPIO.setup(self.r_right, GPIO.IN, GPIO.PUD_UP) 

      def sw_callback(self):
          subprocess.call('sudo shutdown -h now', shell=True)
      #
      # detect shutdown sw push
      GPIO.add_event_detect(self.SHUTDOWN, GPIO.FALLING,bouncetime=250)
      # when the sw was pushed, call the 'call back routine' 
      GPIO.add_event_callback(self.SHUTDOWN, sw_callback) 

      # direction switch detection
      GPIO.add_event_detect(self.r_left, GPIO.FALLING, bouncetime=300)
      GPIO.add_event_detect(self.r_right, GPIO.FALLING, bouncetime=300)
      # callback routine definition
      GPIO.add_event_callback(self.r_left, self.dir_sw_callback)
      GPIO.add_event_callback(self.r_right, self.dir_sw_callback)

  def dir_sw_callback(self, i_pin):
      if i_pin == self.r_left:
        while GPIO.input(self.r_left) == 0:
          if GPIO.input(self.r_right) != 0:
            self.rotate(-1)   # cw
            time.sleep(0.03)
      else:
        while GPIO.input(self.r_right) == 0:
          if GPIO.input(self.r_left) != 0:
            self.rotate(1)    # ccw        
            time.sleep(0.03) 
    
  def rotate(self, r_dir):
# Define advanced sequence
# as shown in manufacturers datasheet
      Seq = [[1,0,0,1],
             [1,0,0,0],
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1]]
       
      StepCount = len(Seq)
      StepDir = r_dir # Set to 1 or 2 for clockwise
                  # Set to -1 or -2 for anti-clockwise

# Wait time
      WaitTime = 10/float(1000)

# Initialise variables
      StepCounter = 0

# Start main lcls
      for count in range(64):
        for pin in range(0, 4):
          xpin = self.StepPins[pin]
          if Seq[StepCounter][pin]!=0:
#            print(" Enable GPIO %i" %(xpin))
            GPIO.output(xpin, True)
          else:
            GPIO.output(xpin, False)

        StepCounter += StepDir

# If we reach the end of the sequence
# start again
        if (StepCounter>=StepCount):
            StepCounter = 0
        if (StepCounter<0):
            StepCounter = StepCount+StepDir

# Wait before moving on
        time.sleep(WaitTime)
# motor power off
      for pin in self.StepPins:
        GPIO.output(pin, False)

  def callback(self):
      while True:
          time.sleep(1)
#
# to make "motor_drive" class instance
#
md = motor_drive()
# wait for sw falling edge
md.callback()
