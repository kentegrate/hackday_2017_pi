from flask import Flask, request
import rospy
from std_msgs.msg import String, Float64

app = Flask(__name__)
arm_pubs = []
table_pub = None
furikake_pub = None
STEP = 10
import time
place_matrix = [[325, 384, 280, 487, 348],
                [325, 325, 280, 433, 348],
                [249, 348, 249, 492, 451],
                [249, 334, 280, 438, 433]]
current_arm = [325, 384, 280, 487, 348, 300]
@app.route("/obento")
def obento_make():
    bento_id = requests.args.get('id', default=0, type=int)
    return "making obento id " + bento_id

@app.route("/place")
def control():
    place_to = request.args.get('to', default=0, type=int)
    go_to(place_to)
    return "going to " + str(place_to)

@app.route("/furikake")    
def furikake():
    cmd = requests.args.get('cmd', default='stop', type=str)
    if cmd =='start':
        pass
    else:##stop
        pass
    return "placing furikake"
def open_hand():
    move_arm(5, 231)

def move_arm_gradual(idx, value):
    value = int(value)
    next_value = current_arm[idx]

    if current_arm[idx] < value:
        next_value = min(current_arm[idx] + STEP, value)
    else:
        next_value = max(current_arm[idx] - STEP, value)
    move_arm(idx, next_value)
    print(str(value) + "," + str(current_arm[idx]))
    print(int(current_arm[idx]) == int(value))
    return int(current_arm[idx]) == int(value)


def move_arm(idx, value):
    global arm_pubs
    arm_pubs[idx].publish(value)
    current_arm[idx] = value
            
def go_to(idx):
    if idx < 0 or idx > len(place_matrix[0])-1:
        idx = 0
    finish_mat = [False] * 5
    while not all(finish_mat):
        for i in range(5):
            finished = move_arm_gradual(i, place_matrix[idx][i])
            finish_mat[i] = finished
        time.sleep(0.1)

def go_home():
    arm_pubs[0].publish(325)
    arm_pubs[1].publish(384)
    arm_pubs[2].publish(280)
    arm_pubs[3].publish(487)
    arm_pubs[4].publish(348)
    open_hand()

    
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
