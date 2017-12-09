from flask import Flask
import rospy
from std_msgs.msg import String

app = Flask(__name__)
pub = None
import time
@app.route("/")
def hello():

    pub.publish("Hello world")
    return "Hello world"
@app.route("/init")
def init_node():
    global pub
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('chatter', String, queue_size=10)    
    return "init ROS OK"
if __name__ == "__main__":
    app.run(port=3000)
