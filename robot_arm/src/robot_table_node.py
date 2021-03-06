from __future__ import division
import rospy
from std_msgs.msg import Float64
import RPi.GPIO as GPIO
from time import sleep
step_motor = None
class DRV8853:
    def __init__(self, PinA1, PinA2, PinB1, PinB2):
        self.mPinA1 = PinA1     #GPIO Number
        self.mPinA2 = PinA2     #GPIO Number
        self.mPinB1 = PinB1     #GPIO Number
        self.mPinB2 = PinB2     #GPIO Number
        self.mStep = 535       
        #self.position = 0 # 0:front, 1:mid, 2:back
        
        self.SetWaitTime(0.01)
        
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.mPinA1, GPIO.OUT)
        GPIO.setup(self.mPinA2, GPIO.OUT)
        GPIO.setup(self.mPinB1, GPIO.OUT)
        GPIO.setup(self.mPinB2, GPIO.OUT)
        
        GPIO.output(self.mPinA2,GPIO.HIGH)
        GPIO.output(self.mPinB2,GPIO.HIGH)
    
    def SetWaitTime(self, wait):
        if wait < 0.01:
            self.mStep_wait = 0.002
        elif wait > 0.5:
            self.mStep_wait = 0.1
        else:
            self.mStep_wait = wait

    def Step_CW(self):
        GPIO.output(self.mPinA1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinB1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinA1,GPIO.LOW)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinB1,GPIO.LOW)
        sleep(self.mStep_wait)
    
    def Step_CCW(self):
        GPIO.output(self.mPinB1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinA1,GPIO.HIGH)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinB1,GPIO.LOW)
        sleep(self.mStep_wait)
        GPIO.output(self.mPinA1,GPIO.LOW)
        sleep(self.mStep_wait)
    
    def SetPosition(self, step, duration):
        diff_step = step - self.mStep
        print(diff_step)
        if diff_step != 0:
            wait = abs(float(duration)/float(diff_step)/4)
            #wait = float2/25
            print("duration:"+str(duration))
            print("diff_step:"+str(diff_step))
            print("wait:"+str(wait))
            self.SetWaitTime(wait)
        for i in range(abs(diff_step)):
            if diff_step > 0:
                self.Step_CW()
            if diff_step < 0:
                self.Step_CCW()
        self.mStep = step
    
    def Cleanup(self):
        GPIO.cleanup()

def stepper_pulse_callback(msg):
    pulse = int(msg.data)
    print(pulse)
    if pulse == 2:
        step_motor.SetPosition(535,1)
        sleep(1)
    elif pulse == 1:
        step_motor.SetPosition(70,1)
        sleep(1)
    elif pulse == 0:
        step_motor.SetPosition(0,1)
        sleep(1)


if __name__ == "__main__":
    rospy.init_node('robot_table_node')
    rospy.Subscriber("robot_table/pulse", Float64, callback=stepper_pulse_callback)
    step_motor = DRV8853(PinA1=4, PinA2=17, PinB1=27, PinB2=22)
    step_motor.SetPosition(535,5)
    rospy.spin()
    step_motor.Cleanup()
