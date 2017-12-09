from flask import Flask, request
import rospy
from std_msgs.msg import String, Float64

app = Flask(__name__)
arm_pubs = []
table_pub = None
furikake_pub = None
import time
@app.route("/pose")
def control():
    place_to = request.args.get('to', default=0, type=int)
    go_to(place_to)

@app.route("/furikake")    
def furikake():
    cmd = requests.args.get('cmd', default='stop', type=str)
    if cmd =='start':
        pass
    else:##stop
        pass

def go_to(idx):
    if idx == 0:
        go_home()
    elif idx == 1:
        pass
    elif idx == 2:
        pass
    elif idx == 3:
        pass
    elif idx == 4:
        pass
    else:
        go_home()

def go_home():
    pass

@app.route("/init")
def init_node():
    global pub
    rospy.init_node('webserver', anonymous=True)
    for i in range(6):
        port = i
        arm_pubs.append(rospy.Publisher("robot_arm/pulse/" + str(port), Float64, queue_size=10))
    furikake_pub = rospy.Publisher("robot_furikake/pulse", Float64, queue_size=10)
    table_pub = rospy.Publisher("robot_table/pulse", Float64, queue_size=10)
    return "init ROS OK"
if __name__ == "__main__":
    app.run(port=3000)
