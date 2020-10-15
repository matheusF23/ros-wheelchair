import rospy as rp
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

rp.init_node('wheelchairControl')

odom - Odometry()

def pose_callBack(msg):
    global odom
    odom = msg

sub = rp.Subscriber('/base_pose_ground_truth', Odometry, pose_callBack)

rp.spin()
