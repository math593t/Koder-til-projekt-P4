#include <wire.h>
#include "BluetoothSerial.h"

// Indstiller adressen til IMU
const int MPU_ADDR = 0x68;
//Indstil samplingsfrekvens
#define SAMPLING_FREQ_HZ 50;
const unsigned long sampleInterval = 1000000 / SAMPLING_FREQ_HZ; 
unsigned long previousMicros = 0;

//Objekter
BluetoothSerial SerialBT;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  //Starter I2C connection
  Wire.begin();
  //Vækker IMU
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); //Adresse for power management
  Wire.write(0); //0 vækker sensor
  Wire.endTransmission(true);

  // Start bluetooth
  SerialBT.begin("ESP32_IMU_Data");
  Serial.println("Bluetooth startet. Klar til at pair.")
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long currentMicros = micros()
  if (currentMicros - previousMicros >= sampleInterval) {
    previousMicros = currentMicros;

    //Starter med at læse accelerometerdata
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);
    Wire.endTransmission(false); //repeated start

    //Anmoder om at læse 14 bytes (De som kan hentes fra IMU)
    Wire.requestFrom(MPU_ADDR, 14, true);

    //Læs data ind
    int16_t rawAccX = (Wire.read() << 8 | Wire.read());
    int16_t rawAccY = (Wire.read() << 8 | Wire.read());
    int16_t rawAccZ = (Wire.read() << 8 | Wire.read());
    int16_t rawAccTemp = (Wire.read() << 8 | Wire.read());
    int16_t rawGyroX = (Wire.read() << 8 | Wire.read());
    int16_t rawGyroY = (Wire.read() << 8 | Wire.read());
    int16_t rawGyroZ = (Wire.read() << 8 | Wire.read());
    
    String dataString = String(rawAccX) + " " + 
                        String(rawAccY) + " " + 
                        String(rawAccZ) + " " +
                        String(rawGyroX) + " " + 
                        String(rawGyroY) + " " + 
                        String(rawGyroZ);

    // Send data over Bluetooth
    SerialBT.println(dataString);
  }
}
