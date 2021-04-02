#include <ros/ros.h>
#include "wiringPi.h"

#include <string>
#include <iostream>
#include <sstream>

using namespace std;

int pin = 17;

void processMsg(ros::NodeHandle nh_)
{
  string str;

  while(nh_.ok()) {
    ROS_INFO("Type 0 or 1");

    getline(cin, str);
    if (str[0] == '0') {
      ROS_INFO("End");
      /* Do something with pin */
      digitalWrite(pin, LOW);
    }
    else if (str[0] == '1') {
      ROS_INFO("Start");
      /* Do something with pin */
      digitalWrite(pin, HIGH);
    }
    else {
      ROS_INFO("Invalid command");
    }
    ros::Duration(1.0).sleep();
  }
}

int main(int argc, char* argv[])
{
  ros::init(argc, argv, "check_node");
  ros::NodeHandle nh;

  wiringPiSetupGpio();

  pinMode(pin, OUTPUT);

  ROS_INFO("Checking has started.");

  processMsg(nh);

  return 0;
}
