/***************************************************************************
  This is a library for the AMG88xx GridEYE 8x8 IR camera

  This sketch tries to read the pixels from the sensor

  Designed specifically to work with the Adafruit AMG88 breakout
  ----> http://www.adafruit.com/products/3538

  These sensors use I2C to communicate. The device's I2C address is 0x69

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Dean Miller for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include <Wire.h>
#include <Servo.h>
#include <Adafruit_AMG88xx.h>

#define PIN_SERVO 3

Servo myservo;

Adafruit_AMG88xx amg;

float pixels[AMG88xx_PIXEL_ARRAY_SIZE];

void setup() {
    Serial.begin(9600);
    Serial.println(F("AMG88xx pixels"));

    bool status;

    myservo.attach(PIN_SERVO);
    
    // default settings
    status = amg.begin();
    if (!status) {
        Serial.println("Could not find a valid AMG88xx sensor, check wiring!");
        while (1);
    }
    
    Serial.println("-- Pixels Test --");

    Serial.println();

    delay(100); // let sensor boot up
}

void serialPrint() {
  //read all the pixels
    amg.readPixels(pixels);

    Serial.print("[");
    for(int i=1; i<=AMG88xx_PIXEL_ARRAY_SIZE; i++){
      Serial.print(pixels[i-1]);
      Serial.print(",");
      if( i%8 == 0 && i != 64 ) Serial.println();
    }
    Serial.println("]");
}

void loop() { 
    myservo.write(90);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(50);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(10);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(50);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(90);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(130);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(170);
    delay(200);
    serialPrint();
    delay(200);
    myservo.write(130);
    delay(200);
    serialPrint();
    delay(200);
}
