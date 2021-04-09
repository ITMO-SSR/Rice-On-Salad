#!/usr/bin/env python
import rospy
import serial
from geometry_msgs.msg import Twist

arduino_name = "/dev/ttyACM0"

serial_port = serial.Serial(arduino_name, 9600)
serial_port.flush()

def bound(value):
  return 7 if value > 7 else -7 if value < -7 else value

def bound1(value):
  sign = "1" if value >= 0 else "0"
  absolute = str(abs(value)) if abs(value) < 100 else "100"
  absolute = "0" * (3 - len(absolute)) + str(absolute)
  return sign + str(absolute)

def encode(linear, angular):
  left = "1000"
  right = "1000"

  sign = "1" if linear >= 0 else "0"
#  rospy.loginfo("left = %f, right = %f", left, right)

#  rospy.loginfo("sign = %f, linear = %f, s | l = %f, b(s | l) = %f", left, right, sign | linear, bound$
  if angular == 0:
    left = right = bound1(linear)
  elif angular > 0:
    if linear == 0:
      right = sign + "090"
    else:
      left = bound1(linear - angular)
      right = bound1(linear + angular)
  else:
    if linear == 0:
      left = sign + "090"
    else:
      left = bound1(linear + angular)
      right = bound1(linear - angular)

 # rospy.loginfo("left = %f, right = %f", left, right)


#  rospy.loginfo("sign = %f, linear = %f, s | l = %f, b(s | l) = %f", left, right, sign | linear, bound$
  if angular == 0:
    left = right = bound1(linear)
  elif angular > 0:
    if linear == 0:
      right = sign + "090"
    else:
      left = bound1(linear - angular)
      right = bound1(linear + angular)
  else:
    if linear == 0:
      left = sign + "090"
    else:
      left = bound1(linear + angular)
      right = bound1(linear - angular)

 # rospy.loginfo("left = %f, right = %f", left, right)

  #rospy.loginfo("sign = %f, linear = %f, s | l = %f, b(s | l) = %f", left, right, sign | linear, bound$
  return str(left) + str(right)

def callback(msg):
  linear_vel = int(msg.linear.x / 0.01)
  angular_vel = int(msg.angular.z / 0.02)

  rospy.loginfo("Received: lin = %f, ang = %f", linear_vel, angular_vel)

  num = encode(linear_vel, angular_vel)
  stroka = num + "\n"

  rospy.loginfo(stroka)
  serial_port.write(stroka)

def listener():
  rospy.init_node('control_node')
  rospy.Subscriber("/cmd_vel", Twist, callback)

  rospy.loginfo("control_node started working")

  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass
