#include <AccelStepper.h>

AccelStepper LeftStepper(1, 2, 5); // pin 2 = step, pin 5 = direction
AccelStepper RightStepper(1, 3, 6); // pin 3 = step, pin 6 = direction

int Lspeed;
int Rspeed;

uint32_t Time;
uint32_t timeSaver;

int RSpeedAr[6] = {0, -700, 0, 700, 500, 0};
int LSpeedAr[6] = {0, 700, 500, -700, 0, 0};

int i;

boolean PiSignal;
int flag;

void setup() {
  pinMode(8, OUTPUT);
  pinMode(4, INPUT);
  LeftStepper.setMaxSpeed(1500);
  LeftStepper.setAcceleration(5000);
  RightStepper.setMaxSpeed(1500);
  RightStepper.setAcceleration(5000);
  digitalWrite(8, LOW);
  flag = 0;
  i = 0;
  Lspeed = 0;
  Rspeed = 0;
  Time = -2000;
  timeSaver = 0;
}

void loop() {
  PiSignal = digitalRead(4) == HIGH;
  if (!PiSignal) {
    if (flag == 0) {
      flag = 1;
      timeSaver = millis() - Time;
      LeftStepper.setSpeed(0);
      RightStepper.setSpeed(0);
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
      digitalWrite(8, HIGH);
    }
  } else {
    if (flag == 1) {
      flag = 0;
      digitalWrite(8, LOW);
      Time = millis() - timeSaver;
      LeftStepper.setSpeed(Lspeed);
      RightStepper.setSpeed(Rspeed);
      if (i == 7) {
        i = 0;
      }
    }
    if ((millis() - Time >= 2000) && (i < 6)) {
      Time = millis();
      Lspeed = LSpeedAr[i];
      Rspeed = RSpeedAr[i];
      LeftStepper.setSpeed(Lspeed);
      RightStepper.setSpeed(Rspeed);
      i++;
    }
    if (i != 7) {
      LeftStepper.runSpeed();
      RightStepper.runSpeed();
    }
    if (i == 6) {
      i = 7;
      digitalWrite(8, HIGH);
    }
  }
}
