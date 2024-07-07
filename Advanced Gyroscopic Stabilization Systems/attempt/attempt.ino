#include <SPI.h>
#include <Wire.h>

unsigned long previousTime = 0;
float previousAngle = 0;
float currentAngle, angleChange, timeInterval, velocity;

void setup() {
  SPI.begin();
  SPI.beginTransaction(SPISettings(10000000, MSBFIRST, SPI_MODE1));
  Serial.begin(9600);
}

unsigned int readAS5047P() {
  SPI.transfer16(0xFFFF); // Dummy write to initiate reading
  return SPI.transfer16(0x0000) & 0x3FFF; // Read the data
}


void loop() {
  unsigned int angleData = readAS5047P(); // Read angle data
  currentAngle = (angleData * 360.0) / 16384.0; // Convert to degrees

  unsigned long currentTime = millis(); // Current time in milliseconds
  timeInterval = (currentTime - previousTime) / 1000.0; // Time interval in seconds

  if (timeInterval >= 0.1) { // Calculate velocity every 0.1 seconds
    angleChange = currentAngle - previousAngle;
    velocity = angleChange / timeInterval; // Velocity in degrees/second

    Serial.print("Angle: ");
    Serial.print(currentAngle);
    Serial.print(" degrees, Velocity: ");
    Serial.print(velocity);
    Serial.println(" degrees/second");

    previousTime = currentTime;
    previousAngle = currentAngle;
  }

  delay(10); // Short delay for stability
}


