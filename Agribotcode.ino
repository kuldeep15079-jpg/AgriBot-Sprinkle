 
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <Servo.h>

// -------- I2C LCD --------
LiquidCrystal_I2C lcd(0x27, 16, 2);

// -------- DHT11 --------
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// -------- Soil Moisture --------
#define SOIL_PIN A0

// -------- Motor Driver (7,6,5,4) --------
#define IN1 7
#define IN2 6
#define IN3 5
#define IN4 4

// -------- Servos (13,12) --------
#define SERVO1_PIN 13
#define SERVO2_PIN 12

Servo servo1;
Servo servo2;

char btData;

// -------- Motor Functions --------
void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void setup() {

  // Motor setup
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Servo setup
  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);

  // Continuous rotation start
  servo1.write(0);     // rotate continuously
  servo2.write(180);   // rotate continuously opposite

  // Sensors
  dht.begin();
  pinMode(SOIL_PIN, INPUT);

  // LCD
  lcd.init();
  lcd.backlight();

  Serial.begin(9600);
}

void loop() {

  // -------- Bluetooth Control --------
  if (Serial.available() > 0) {
    btData = Serial.read();

    if (btData == 'A') moveForward();
    else if (btData == 'B') moveBackward();
    else if (btData == 'L') turnLeft();
    else if (btData == 'R') turnRight();
    else if (btData == 'S') stopMotors();
  }

  // -------- Sensor Reading --------
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilValue = analogRead(SOIL_PIN);

  int soilPercent = map(soilValue, 1023, 0, 0, 100);

  // -------- LCD Display --------
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temperature);
  lcd.print("C H:");
  lcd.print(humidity);

  lcd.setCursor(0, 1);
  lcd.print("Soil:");
  lcd.print(soilPercent);
  lcd.print("%");

  delay(2000);
}