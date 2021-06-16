#!/usr/bin/env python
import math
import rospy
import serial
from sensor_msgs.msg import LaserScan

arduino_name = "/dev/ttyACM0" # Порт, через который происходит взаимодействие с Arduino

serial_port = serial.Serial(arduino_name, 9600) # Подключаемся по UART к Arduino
serial_port.flush() # Очищаем канал передачи данных

dist_forward_min = 0.3 # Минимальное расстояние до ближайшего предмета спереди
dist_backward_min = 0.3 # Минимальное расстояние до ближайшего предмета сзади
dist_medium = 0.35 # Если расстояние до ближайшего объекта меньше данной, то робот снижает скорость

angle_forward = 0.4 # Половина угла обзора спереди
angle_backward = 0.5 # Половина угла обзора сзади

state_cur = "0" # Текущее состояние

def find_min(ranges): # Функция, возвращающая минимальное расстояние и его индекс в списке ranges
  min_current = 1000000
  index_current = -1
  for i, e in list(enumerate(ranges)):
    if e < min_current:
      min_current = e
      index_current = i
  return (index_current, min_current)

def compute_signal(index, range, msg): # Функция расчета текущего состояния
  angle_min = msg.angle_min # Начальный угол сканирования
  angle_max = msg.angle_max # Конечный угол сканирования
  angle_current = (angle_max - angle_min) / len(msg.ranges) * index # Угол, соответствующий ближайшему объекту

  if range > dist_forward_min and range < dist_medium: # Снижаем скорость
    signal = "4"
  elif range < dist_forward_min and abs(angle_current) < angle_forward: # Вперед ехать нельзя
    signal = "1"
  elif range < dist_backward_min and abs(math.pi - angle_current) < angle_backward: # Назад ехать нельзя
    signal = "2"
  else: # Можно спокойно двигаться
    signal = "0"

  return signal

def callback(msg): # Коллбэк, который выполняется при получении новых сообщений из топика
  global state_cur

  ranges = msg.ranges # расстояния до объектов, полученные с лидара
  tup = find_min(ranges)
  rospy.loginfo("Received: index = %f, range = %f", tup[0], tup[1])

  signal = compute_signal(tup[0], tup[1], msg)
  rospy.loginfo("Signal = " + signal)

  if signal != state_cur: # Если состояние изменилось, передаем сообщение на Arduino
    rospy.loginfo("New state = " + signal)
    state_cur = signal
    encoded_str = signal + "#"
    serial_port.write(encoded_str)

def listener():
  rospy.init_node("distance_node") # Инициализируем ROS-ноду
  rospy.Subscriber("/scan", LaserScan, callback) # Подписываемся на топик /scan
  rospy.loginfo("distance_node started working")
  rospy.spin() # Нужно, чтобы ROS не завершил работу раньше времени

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass