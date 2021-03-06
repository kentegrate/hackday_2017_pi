from flask import Flask, request
import rospy
from std_msgs.msg import String, Float64

app = Flask(__name__)
arm_pubs = []
table_pub = None
furikake_pubs = []
init_ok = False
STEP = 10
import time
place_matrix = [[325, 384, 280, 487, 348],
                [330, 285, 294, 433, 366],
                [217, 339, 285, 465, 442],
                [222, 352, 330, 442, 442],
                [312, 375, 384, 460, 366]]
#294, 438 , 130, 242
furikake_matrix = [[294,130],
                   [294,130],
                   [438,130],
                   [438,242],
                   [294,242],
                   [294,242],
                   [438,130],
                   [438,130],
                   [294,130],
                   [294,242],
                   [438,242],
                   [438,242],
                   [438,130],
                   [438,130],
                   [294,130],
                   [294,242],
                   [438,242],
                   [438,242],
                   [600,275]]

current_arm = [325, 384, 280, 487, 348, 300]
@app.route("/obento")
def obento_make():
    bento_id = request.args.get('id', default=0, type=int)
    move_stage_osozai()
#    time.sleep(10)
    if bento_id == 0:
        go_to(0)
        open_hand()
        go_to(1)
        close_hand()
        go_to(0)
        go_to(2)
        go_to(3)
        open_hand()
        go_to(2)
        go_to(0)
    else:
        go_to(0)
        open_hand()
        go_to(4)
        close_hand()
        go_to(0)
        go_to(2)
        go_to(3)
        open_hand()
        go_to(2)
        go_to(0)
    move_stage_gohan()
    time.sleep(1)
    furikake()
#    time.sleep(10)
    move_stage_init()
#    time.sleep(1)
        
    return "making obento id " + str(bento_id)

@app.route("/place")
def control():
    place_to = request.args.get('to', default=0, type=int)
    go_to(place_to)
    return "going to " + str(place_to)

@app.route("/furikake")    
def furikake():
    for furikake_cmd in furikake_matrix:
        for i in range(2):
            furikake_pubs[i].publish(furikake_cmd[i])
            time.sleep(0.05)
    return "placing furikake"
@app.route("/open")
def open_hand():
    move_arm(5, 231)
    time.sleep(1)
    return "open arm"
@app.route("/close")    
def close_hand():
    move_arm(5, 487)
    time.sleep(1)    
    return "close arm"

def move_stage(idx):
    global table_pub
    table_pub.publish(idx)

@app.route("/stage/init")
def move_stage_init():
    move_stage(2)
    return "moving table to initial position"

@app.route("/stage/gohan")
def move_stage_gohan():
    move_stage(1)
    return "moving table to gohan position"

@app.route("/stage/osozai")
def move_stage_osozai():
    move_stage(0)
    return "moving table to osozai position"

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
    global init_ok
    global table_pub
    if init_ok:
        return "already init ok"
    global pub
    rospy.init_node('webserver', anonymous=True)
    for i in range(6):
        port = i
        arm_pubs.append(rospy.Publisher("robot_arm/pulse/" + str(port), Float64, queue_size=10))
    for i in range(2):
        port = i + 6
        furikake_pubs.append(rospy.Publisher("robot_arm/pulse/" + str(port), Float64, queue_size=10))
    table_pub = rospy.Publisher("robot_table/pulse", Float64, queue_size=10)
    time.sleep(1)
    init_ok = True
    return "init ROS OK"
if __name__ == "__main__":
    app.run('0.0.0.0', port=3000)
