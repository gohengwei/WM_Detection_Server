#include <XBee.h>
#include <SPI.h>
#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"
#include <stdlib.h>

//Constants
#define LED_IND A1
#define READ_TIMEOUT 7
#define XBEE_INTERVAL 0
#define XBEE_NUM 3
#define XBEE_TRIG 1

//Xbee Set up
uint8_t payload[] = {4};
XBee xbees[XBEE_NUM];
Rx16Response rx16s[XBEE_NUM];

//Hardware Set up
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();


//Variables to be used
uint32_t time = 0;
byte color = 1;
int rssi = 53, delayVal = 0;
bool isMotion =true,endCheck=false;
byte cur_rssi[3] = {0,0,0};
byte old_rssi[3] = {0,0,0};
uint32_t time_rssi[3] = {0,0,0}, endCtr =0;;
bool checkAna = true,startSend = false;
bool matrixActive = false;

static uint8_t __attribute__ ((progmem)) smile_bmp[]={0x3C, 0x42, 0x95, 0xA1, 0xA1, 0x95, 0x42, 0x3C};
static uint8_t __attribute__ ((progmem)) frown_bmp[]={0x3C, 0x42, 0xA5, 0x91, 0x91, 0xA5, 0x42, 0x3C};

int freeRam () {
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

void setup()
{

  /* add setup code here */
	//Initialize various hardware
	//Initialize Arduino Serial Ports
	Serial.begin(115200);
	Serial1.begin(57600);
	Serial2.begin(57600);
	Serial3.begin(57600);
	//Initialize Xbees
	xbees[0].setSerial(Serial1);
	xbees[1].setSerial(Serial2);
	xbees[2].setSerial(Serial3);

	//Initialize Matrix
	matrix.begin(0x70);  // pass in the address

	//pinMode(LED_IND,OUTPUT);
	blink_Matrix();

}

void loop()
{
	
	collectData();
	//Check for fluctuations by checking for gradient changes
	byte val = abs(cur_rssi[XBEE_TRIG] - old_rssi[XBEE_TRIG]);
	if(val < 3) checkAna = false;
	else checkAna = true;
	old_rssi[XBEE_TRIG] = cur_rssi[XBEE_TRIG];
	
	//If there are fluctuations in frequency detected
	if(checkAna  && val < 30)
	{
		if(!startSend)	
		{
			Serial.write("{");
			startSend = true;
		}
		endCheck = true;
		//isMotion = true;
		endCtr = 0;
	}

	//If there are no longer anymore fluctuations in frequency
	if(!checkAna && endCheck)	
	{
		if(endCtr >500)	
		{
			startSend = false;
			endCheck = false;
			//isMotion = false;
			Serial.print('}');
			endCtr = 0;
			blink_Matrix();
		} else
			endCtr++;
	}

	if(matrixActive) check_Matrix();

}

void collectData()
{
	//collectData();
	for(int i = 0; i<XBEE_NUM;i++)
	{
		rx16s[i] = Rx16Response();
		xbees[i].readPacket(READ_TIMEOUT) ;
		if (xbees[i].getResponse().isAvailable()) {
			if (xbees[i].getResponse().getApiId() == RX_16_RESPONSE) {
				xbees[i].getResponse().getRx16Response(rx16s[i]);
				rssi = rx16s[i].getRssi();
				cur_rssi[i] = rssi;
				if(isMotion)
				{
					Serial.write(rssi);
					Serial.write(millis() - time_rssi[i]);
					//Serial.print(" ");
				}
				time_rssi[i] =millis();
			}
		} else
		{
				if(isMotion)
				{
					//Serial.print("e: ");
					Serial.write(cur_rssi[i]);
					Serial.write(millis() - time_rssi[i]);
				}
		}
	}
	

	//Serial.println();
	if(isMotion) 
		{
			Serial.print("\n");
		}
	delay(XBEE_INTERVAL);
}

void blink_LED()
{
	digitalWrite(LED_IND,HIGH);
	delay(250);
	digitalWrite(LED_IND,LOW);
	delay(250);
}

void blink_Matrix()
{
	matrix.clear();
	matrix.drawBitmap(0, 0, smile_bmp, 8, 8, color);
	matrix.writeDisplay();
	color++;
	if(color >3) color = 1;
	matrixActive = true;
}

void check_Matrix()
{
	if(delayVal > 200)
	{
		delayVal = 0;
		matrix.clear();
		matrixActive  = false;
		matrix.writeDisplay();  // write the changes we just made to the display
	} else delayVal++;
}