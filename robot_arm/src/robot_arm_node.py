from __future__ import division
import rospy
from std_msgs.msg import Float64
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
def servo_pulse_callback(msg, port):
    pulse = int(msg.data)
    pwm.set_pwm(port, 0, pulse)

def servo_angle_callback(msg, port):
    angle = msg.data
    pulse = angle2pulse(angle)
    pwm.set_pwm(port, 0, pulse)

SERVO_MIN_PULSE = 150
SERVO_MAX_PULSE = 600
SEVRO_MIN_ANGLE = -90
SERVO_MAX_ANGLE = 90

def angle2pulse(angle):
    if angle > SERVO_MAX_ANGLE: angle = SERVO_MAX_ANGLE
    if angle < SERVO_MIN_ANGLE: angle = SERVO_MIN_ANGLE
    pulse = 1.0 * (SERVO_MAX_PULSE - SERVO_MIN_PULSE) * (angle - SERVO_MIN_ANGLE) / (SERVO_MAX_ANGLE - SERVO_MIN_ANGLE) + SERVO_MIN_PULSE
    # remap angle to pulse length
    return int(pulse)
    
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

if __name__ == "__main__":
    rospy.init_node('robot_arm_node')
    for i in range(8):
        port = i
        rospy.Subscriber("robot_arm/angle/" + str(port), Float64, callback=servo_angle_callback, callback_args=port)
        rospy.Subscriber("robot_arm/pulse/" + str(port), Float64, callback=servo_pulse_callback, callback_args=port)
    rospy.spin()
