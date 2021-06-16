#!/usr/bin/env python
import rospy
import serial
from geometry_msgs.msg import Twist

arduino_name = "/dev/ttyACM0" # Порт, через который происходит взаимодействие с Arduino

serial_port = serial.Serial(arduino_name, 9600) # Подключаемся по UART к Arduino
serial_port.flush() # Очищаем канал передачи данных

def bound(value): # Функция, возвращающая закодированное значение скорости
  upper_bound = 100

  sign = "1" if value >= 0 else "0" # 1 - движение вперед, 0 - движение назад
  absolute = str(abs(value)) if abs(value) < upper_bound else str(upper_bound)

  absolute = "0" * (3 - len(absolute)) + absolute # Добавляем недостающие нули

  return sign + absolute

def encode(linear, angular): # Функция для расчета сигнала, передаваемого на Arduino
  left = "1000"
  right = "1000"

  direct_speed = 90

  if angular == 0: # Робот едет прямо
    left = right = bound(linear)
  elif angular > 0:
    if linear == 0: # Робот поворачивается вокруг своей оси вправо
      left = bound(direct_speed)
    else: # Робот движется с уклоном влево
      left = bound(linear - angular)
      right = bound(linear + angular)
  else:
    if linear == 0: # Робот поворачивается вокруг своей оси влево
      right = bound(direct_speed)
    else: # Робот движется с уклоном вправо
      left = bound(linear + angular)
      right = bound(linear - angular)

  return left + right

def callback(msg): # Коллбэк, который выполняется при получении новых сообщений из топика
  linear_vel = int(msg.linear.x / 0.01) # Линейная скорость
  angular_vel = int(msg.angular.z / 0.1) # Угловая скорость

  rospy.loginfo("Received: lin = %f, ang = %f", linear_vel, angular_vel)

  num = encode(linear_vel, angular_vel) # Закодированные скорости, передаваемые на Arduino
  encoded_str = num + "\n"

  rospy.loginfo(encoded_str)
  serial_port.write(encoded_str)

def listener():
  rospy.init_node('control_node') # Инициализируем ROS-ноду
  rospy.Subscriber("/cmd_vel", Twist, callback) # Подписываемся на топик cmd_vel
  rospy.loginfo("control_node started working")
  rospy.spin() # Нужно, чтобы ROS не завершил работу раньше времени

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass
