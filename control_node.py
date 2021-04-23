#!/usr/bin/env python
import rospy
import serial
from geometry_msgs.msg import Twist

arduino_name = "/dev/ttyACM0"

serial_port = serial.Serial(arduino_name, 9600)
serial_port.flush()

def bound(value):
  upper_bound = 100

  sign = "1" if value >= 0 else "0"
  absolute = str(abs(value)) if abs(value) < upper_bound else str(upper_bound)

  # Add missing digits
  absolute = "0" * (3 - len(absolute)) + absolute

  return sign + absolute

def encode(linear, angular):
  left = "1000"
  right = "1000"

  direct_speed = 90

  if angular == 0:
    left = right = bound(linear)
  elif angular > 0:
    if linear == 0:
      left = bound(direct_speed)
    else:
      left = bound(linear - angular)
      right = bound(linear + angular)
  else:
    if linear == 0:
      right = bound(direct_speed)
    else:
      left = bound(linear + angular)
      right = bound(linear - angular)

  return left + right

def callback(msg):
  # Linear and angular velocities
  linear_vel = int(msg.linear.x / 0.01)
  angular_vel = int(msg.angular.z / 0.1)

  rospy.loginfo("Received: lin = %f, ang = %f", linear_vel, angular_vel)

  num = encode(linear_vel, angular_vel)
  encoded_str = num + "\n"

  rospy.loginfo(encoded_str)
  serial_port.write(encoded_str)

def listener():
  # Init our node
  rospy.init_node('control_node')

  # Subscribe to the cmd_vel
  rospy.Subscriber("/cmd_vel", Twist, callback)

  rospy.loginfo("control_node started working")

  # Keep it alive
  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass
