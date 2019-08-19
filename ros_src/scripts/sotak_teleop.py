#!/usr/bin/env python

import rospy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class Teleop:
    def __init__(self):
        rospy.init_node('zotac_teleop')

        #self.turn_scale = rospy.get_param('~turn_scale')
        #self.drive_scale = rospy.get_param('~drive_scale')
        #self.deadman_button = rospy.get_param('~deadman_button', 0)
        #self.planner_button = rospy.get_param('~planner_button', 1)

        self.cmd = None
        self.joy = Joy()
        self.cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	#self.cmd_pub = rospy.Publisher('husky_velocity_controller/cmd_vel', Twist, queue_size = 1)


        rospy.Subscriber("joy", Joy, self.callback)
        #rospy.Subscriber("plan_cmd_vel", Twist, self.planned_callback)
        #self.planned_motion = Twist()
        
        #rate = rospy.Rate(rospy.get_param('~hz', 20))
	self.rate = rospy.Rate(rospy.get_param('~hz', 20))
        
	rospy.spin()

        #while not rospy.is_shutdown():
            #rate.sleep()
            #if self.cmd:
		#print('hola')
                #self.cmd_pub.publish(self.cmd)

    #def planned_callback(self, data):
        """ Handle incoming Twist command from a planner.
        Manually update motion planned output if the buttons
        are in the right state """
    #    self.planned_motion = data 
    #    if self.joy.buttons[self.deadman_button] == 0 and\
    #       self.joy.buttons[self.planner_button] == 1:
    #        self.cmd = self.planned_motion

    def callback(self, data):
        """ Receive joystick data, formulate Twist message.
        Use planner if a secondary button is pressed """
        self.joy = data
        cmd = Twist()
        #cmd.linear.x = data.axes[1] * 1
        #cmd.angular.z = data.axes[0] * 1

	#self.cmd = cmd

	#print(cmd.linear.x);
	#print(cmd.linear.x);

	#if self.cmd:
		#self.cmd_pub.publish(self.cmd)

	#if data.buttons[0] == 1:
	#	print('hola')
	#	self.cmd = None

	#print(data.axes[0])
	self.rate.sleep()

        #if data.buttons[self.deadman_button] == 1:
	if data.axes[0] or data.axes[1]:
		#cmd.linear.x = data.axes[1] * 2.5
        	#cmd.angular.z = data.axes[0] * 2.5
		cmd.linear.x = data.axes[0] * 2.8
        	cmd.angular.z = data.axes[1] * -2.8
		#cmd.angular.z = data.axes[1] * -2.5
		self.cmd = cmd
        #elif data.buttons[self.planner_button] == 1:
            #self.cmd = self.planned_motion
        else:
		cmd.linear.x = 0
	        cmd.angular.z = 0
		self.cmd = cmd

	self.cmd_pub.publish(self.cmd)

if __name__ == "__main__": Teleop()

