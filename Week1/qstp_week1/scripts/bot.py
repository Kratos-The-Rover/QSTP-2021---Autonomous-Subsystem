#!/usr/bin/env python3

import rospy
from qstp_week1.srv import state_change,state_changeResponse
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from math import pi

class Bot:
    
    def __init__(self):
        self.state = 'stop'
        self.direction = 1
        self.vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.state_service = rospy.Service("bot_state_change", state_change,self.change_state_fn)
        self.vel = Twist()
    
    def change_state_fn(self,req):
        if ((req.state in ['linear','rotate','stop','infinity'])and (req.direction in [1,-1])):
            self.state = req.state
            self.direction = req.direction
            return state_changeResponse(True)
        else:
            return state_changeResponse(False)
    
    def update_vel(self, linear, angular):
        self.vel.linear.x = linear[0]
        self.vel.linear.y = linear[1]
        self.vel.linear.z = linear[2]

        self.vel.angular.x = angular[0]
        self.vel.angular.y = angular[1]
        self.vel.angular.z = angular[2]
    
    def move_forward(self):
        linear = [0.0,0.0,0.0]
        angular = [0.0, 0.0, 0.0]
        if (self.direction==1):
            linear[0] = 0.2
        else:
            linear[0] = -0.2
        self.update_vel(linear,angular)
        self.vel_pub.publish(self.vel)
    
    def rotate_bot(self):
        linear = [0.0,0.0,0.0]
        angular = [0.0, 0.0, 0.0]
        if (self.direction==1):
            angular[2] = 0.2
        else:
            angular[2] = -0.2
        self.update_vel(linear,angular)
        self.vel_pub.publish(self.vel)

    def stop_bot(self):
        linear = [0.0,0.0,0.0]
        angular = [0.0, 0.0, 0.0]
        self.update_vel(linear, angular)
        self.vel_pub.publish(self.vel)

    def infinity_motion(self):
        '''
            BONUS TASK
        '''
        omega = 0.8*self.direction
        margin = -0.1
        linear_vel = 0.2

        time_taken = 2*pi/omega - margin
        r = rospy.Rate(1.0/time_taken)

        linear = [linear_vel, 0.0, 0.0]
        angular = [0.0,0.0,omega]
        self.update_vel(linear, angular)
        self.vel_pub.publish(self.vel)
        r.sleep()
        self.vel.angular.z = -1*omega
        self.vel_pub.publish(self.vel)
        r.sleep()
    
    def bot_main(self):
        if (self.state=='linear'):
            self.move_forward()
        elif (self.state == 'rotate'):
            self.rotate_bot()
        elif (self.state == 'infinity'):
            self.infinity_motion()
        else:
            self.stop_bot()

if __name__=='__main__':
    rospy.init_node('Week1_bot')
    tbot = Bot()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        tbot.bot_main()
        rate.sleep()


