/*
  Alexa Message Client using Bridge
*/

#include <Mailbox.h>
#include <math.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#define PIN 13
Adafruit_NeoPixel strip = Adafruit_NeoPixel(40, PIN, NEO_GRB + NEO_KHZ800);

uint8_t currentBrightness = 60;
uint32_t currentColor = strip.Color(127, 127, 127);

void setup() {
  SerialUSB.println("setup()");
  strip.begin();
  strip.show();
  
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  
  Bridge.begin();
  Mailbox.begin();
  digitalWrite(13, HIGH);

  SerialUSB.begin(9600);

  while (!SerialUSB);
  SerialUSB.println("Setup Complete, Checking for Messages");
}

void loop() {
  String message;
  String content;
  if (Mailbox.messageAvailable()) {
    while (Mailbox.messageAvailable()) {
      Mailbox.readMessage(message);
      SerialUSB.println("\nMessage Received: " + message);

      uint8_t brightness = 0;
      if (message.startsWith("B"))
      {
        SerialUSB.println("Setting Brightness");  
        String content_value;
        content = message.substring(1);

        // If a brightnessDelta request, convert our range from -100-100 to 0-255
        if (content.startsWith("-")) {
          SerialUSB.println("Delta -"); 
          content_value = content.substring(1);
          uint8_t bval = atoi(content_value.c_str());
          SerialUSB.println(bval);
          uint8_t bval_adjusted = map(bval, 0, 100, 0, 255);
          SerialUSB.println(bval_adjusted); 
          if (bval_adjusted < currentBrightness)
            brightness = currentBrightness - bval_adjusted;
          else
            brightness = 0;
        } 
        else if (content.startsWith("+")) {
          SerialUSB.println("Delta +");
          content_value = content.substring(1);
          uint8_t bval = atoi(content_value.c_str());
          SerialUSB.println(bval);
          uint8_t bval_adjusted = map(bval, 0, 100, 0, 255);
          if (bval_adjusted > currentBrightness)
            brightness = currentBrightness + bval_adjusted;
          else
            brightness = 255;
        }
        else {
          // A direct brightness level
          brightness = atoi(content.c_str());
        }

        brightness = constrain(brightness, 0, 255);
        SerialUSB.println(brightness);
        strip.setBrightness(brightness);
        currentBrightness = brightness;
        strip.show();
      } 
      
      if (message.startsWith("C"))
      { 
        SerialUSB.println("Setting Color");   
        content = message.substring(1);

        char* tokenString = const_cast<char *>(content.c_str());
        char* r = strtok(tokenString, "|");
        char* g = strtok(NULL, "|");
        char* b = strtok(NULL, "|");

        // Convert down from 0-255 to 0-127
        uint8_t rval = (uint8_t) (atoi(r) / 2);
        uint8_t gval = (uint8_t) (atoi(g) / 2);
        uint8_t bval = (uint8_t) (atoi(b) / 2);

        SerialUSB.print(rval);
        SerialUSB.print(",");
        SerialUSB.print(gval);
        SerialUSB.print(",");
        SerialUSB.print(bval);
        SerialUSB.println("");

        setColor(strip.Color(rval, gval, bval), true);
      } 

      if (message.startsWith("P")) {
        SerialUSB.println("Setting Power");  
        content = message.substring(1);
        
        
        if (content == "OFF")
        {
          SerialUSB.println("Turning OFF light");
          setColor(strip.Color(0, 0, 0), false);
        }

        if (content == "ON")
        {
          SerialUSB.println("Turning ON light");
          setColor(currentColor, false);
          strip.setBrightness(currentBrightness);
          strip.show();
        }
      }
    }
  }

  // Wait 1 second
  delay(1000);
}

void setColor(uint32_t c, bool store) {
  for(uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
  }
  strip.show();
  if (store)
    currentColor = c;
}

void setSplitColor(uint32_t lc, uint32_t rc) {
  uint8_t half = strip.numPixels() / 2;
  uint8_t wait = 8;
  for(uint16_t i = 0; i < strip.numPixels(); i++) {

    if (i < half) {
      strip.setPixelColor(i, lc);
    }
    else {
      strip.setPixelColor(i, rc);     
    }
    strip.show();
    delay(wait);
  }

}

