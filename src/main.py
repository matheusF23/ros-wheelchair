#!/usr/bin/env python2

import rospy as rp
import tf
import math

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

rp.init_node('wheelchairControl')
pub = rp.Publisher('/cmd_vel', Twist, queue_size=1)

odom = Odometry()
state = 'initial'

def pose_callBack(msg):
    global odom
    odom = msg

def timerCallBack(event):
    global state
    position = odom.pose.pose.position
    quaternion = odom.pose.pose.orientation

    quat = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
    euler = tf.transformations.euler_from_quaternion(quat)
    euler = euler[2]*180.0/math.pi

    msg = Twist()

    if state == 'initial':
        msg.angular.z = 0.5
        if 88 < euler < 92:
            state = 'state1'
            msg.angular.z = 0
    elif state == 'state1':
        msg.linear.x = 1
        if position.y > 24:
            state = 'state2'
            msg.linear.x = 0

    pub.publish(msg)

# timer com 0.1s de periodo (10hz)
timer = rp.Timer(rp.Duration(0.05), timerCallBack)

sub = rp.Subscriber('/base_pose_ground_truth', Odometry, pose_callBack)


rp.spin()
