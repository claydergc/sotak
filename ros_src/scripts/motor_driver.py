#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import serial


class Driver:
    def __init__(self):
        # init ros
        rospy.init_node('car_driver', anonymous=True)
        rospy.Subscriber('/cmd_vel', Twist, self.get_cmd_vel)
        self.ser1 = serial.Serial('/dev/ttyUSB0', 115200) #puerto serie arduino 1
	self.ser2 = serial.Serial('/dev/ttyUSB1', 115200) #puerto serie arduino 2
        self.get_arduino_message()

    # get cmd_vel message, and get linear velocity and angular velocity
    def get_cmd_vel(self, data):
        x = data.linear.x
        angular = data.angular.z
        self.send_cmd_to_arduino1(x, angular)
	self.send_cmd_to_arduino2(x, angular)

    def send_cmd_to_arduino1(self, x, angular):
        # calculate left wheels' signal
        left = int((x - angular) * 50)
        # format for arduino
        message = "V" + str(left)
        print message
        # send by serial 1 
        self.ser1.write(message)

    def send_cmd_to_arduino2(self, x, angular):
        # calculate right wheels' signal
        right = int((x + angular) * 50)
        # format for arduino
        message = "V" + str(right)
        print message
        # send by serial 2
        self.ser2.write(message)

    # receive serial text from arduino and publish it to '/arduino' message
    def get_arduino_message(self):
        pub = rospy.Publisher('arduino', String, queue_size=10)
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            message = self.ser1.readline() + "," + self.ser2.readline()
            pub.publish(message)
            r.sleep()

if __name__ == '__main__':
    try:
        d = Driver()
    except rospy.ROSInterruptException: 
        pass


