#include <AccelStepper.h>

AccelStepper LeftStepper(1, 2, 5); // pin 2 = step, pin 5 = direction
AccelStepper RightStepper(1, 3, 6); // pin 3 = step, pin 6 = direction

int Lspeed;
int Rspeed;
long comand;
boolean PiSignal;
boolean zero;
int flag;
String data;

void setup() {
  pinMode(8, OUTPUT);
  pinMode(4, INPUT);
  LeftStepper.setMaxSpeed(1000);
  LeftStepper.setAcceleration(5000);
  RightStepper.setMaxSpeed(1000);
  RightStepper.setAcceleration(5000);
  digitalWrite(8, LOW);
  Serial.begin(9600);
  flag = 0;
  zero = false;
  Lspeed = 0;
  Rspeed = 0;
  data  = "10000000";
}

void loop() {
  //PiSignal = digitalRead(4)==HIGH;
  //if(!PiSignal){
    //if(flag==0){
      //flag=1;
      //LeftStepper.setSpeed(0);
      //RightStepper.setSpeed(0);
      //LeftStepper.runSpeed();
      //RightStepper.runSpeed();
      //digitalWrite(8, HIGH);
    //}
  //}else{
    //if(flag==1){
      //flag=0;
      //digitalWrite(8, LOW);
    //}
    if (Serial.available()>0){
      String data = Serial.readStringUntil('\n');
      comand = data.toInt();
      //Serial.println(comand);
      Lspeed = calculateSpeed(comand/10000);
      Rspeed = calculateSpeed(comand%10000);
      LeftStepper.setSpeed(Lspeed);
      RightStepper.setSpeed(Rspeed);
    }
    if (!zero){
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
    }
    if(Lspeed==0&&Rspeed==0){
      zero=true;
      digitalWrite(8, HIGH);
    }else if(zero){
      zero=false;
      digitalWrite(8, LOW);
      LeftStepper.setSpeed(Lspeed);
      RightStepper.setSpeed(Rspeed);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
    }
  }
//}

int calculateSpeed(long x)
{
  if (x/1000==1){
    return map(x%1000, 0, 100, 0, 1000);
  }else{
    return map(x%1000, 0, 100, 0, -1000);
  }
}
