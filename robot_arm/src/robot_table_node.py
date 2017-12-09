from __future__ import division
import rospy
from std_msgs.msg import Float64
import time

def stepper_pulse_callback(msg):
    pulse = int(msg.data)
    print(pulse)

if __name__ == "__main__":
    rospy.init_node('robot_table_node')
    rospy.Subscriber("robot_table/pulse", Float64, callback=stepper_pulse_callback)
    rospy.spin()
