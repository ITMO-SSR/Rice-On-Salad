#!/usr/bin/env python
import math
import rospy
import serial
from sensor_msgs.msg import LaserScan

arduino_name = "/dev/ttyACM0"

serial_port = serial.Serial(arduino_name, 9600)
serial_port.flush()

dist_forward_min = 0.3
dist_backward_min = 0.3
dist_medium = 0.35

angle_forward = 0.4
angle_backward = 0.5

state_cur = "0"

def find_min(ranges):
  min_current = 1000000
  index_current = -1
  for i, e in list(enumerate(ranges)):
    if e < min_current:
      min_current = e
      index_current = i
  return (index_current, min_current)

def compute_signal(index, range, msg):
  angle_min = msg.angle_min
  angle_max = msg.angle_max
  angle_current = (angle_max - angle_min) / len(msg.ranges) * index

  if range > dist_forward_min and range < dist_medium:
    signal = "4"
  elif range < dist_forward_min and abs(angle_current) < angle_forward:
    signal = "1"
  elif range < dist_backward_min and abs(math.pi - angle_current) < angle_backward:
    signal = "2"
  else:
    signal = "0"

  return signal

def callback(msg):
  global state_cur

  ranges = msg.ranges
  tup = find_min(ranges)
  rospy.loginfo("Received: index = %f, range = %f", tup[0], tup[1])

  signal = compute_signal(tup[0], tup[1], msg)
  rospy.loginfo("Signal = " + signal)

  if signal != state_cur:
    rospy.loginfo("New state = " + signal)
    state_cur = signal
    encoded_str = signal + "#"
    serial_port.write(encoded_str)

def listener():
  rospy.init_node("distance_node")
  rospy.Subscriber("/scan", LaserScan, callback)
  rospy.loginfo("distance_node started working")
  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass