/*************************************************** 
  This is a library for our I2C LED Backpacks

  Designed specifically to work with the Adafruit LED 7-Segment backpacks 
  ----> http://www.adafruit.com/products/881
  ----> http://www.adafruit.com/products/880
  ----> http://www.adafruit.com/products/879
  ----> http://www.adafruit.com/products/878

  These displays use I2C to communicate, 2 pins are required to 
  interface. There are multiple selectable I2C addresses. For backpacks
  with 2 Address Select pins: 0x70, 0x71, 0x72 or 0x73. For backpacks
  with 3 Address Select pins: 0x70 thru 0x77

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/
 
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"

Adafruit_7segment matrix = Adafruit_7segment();

void setup() {
  Serial.begin(9600);
  Serial.println("7 Segment Backpack Test");

  matrix.begin(0x70);
}

void loop() {
  // try to print a number thats too long
  // print a hex number
  
  matrix.print(0x0100, HEX);
  matrix.writeDigitRaw(0,0x00);
  matrix.writeDigitRaw(1,0b00000110);
  matrix.writeDigitRaw(2,0x00);
  matrix.writeDigitRaw(3,0x00);
  matrix.writeDigitRaw(4,0x00);
  matrix.writeDisplay();
  delay(3000);
  
  matrix.print(0x104E, HEX);
  matrix.writeDigitRaw(0,0b00111000);  
  matrix.writeDigitRaw(3,0b00111110);
  matrix.writeDisplay();
  delay(3000);
  
  matrix.writeDigitRaw(0,0x00);
  matrix.writeDigitRaw(1,0b00111110);
  matrix.writeDigitRaw(2,0x00);
  matrix.writeDigitRaw(3,0b00000000);
  matrix.writeDigitRaw(4,0b11111100);
  matrix.writeDisplay();
  
  delay(10000);
}

