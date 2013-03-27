#include <i2cLCD.h>
#include <XBee.h>
#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include <Servo.h>
#include <stdlib.h>
#include "rssi_constants.h"

//Constants

//Xbee Set up
uint8_t payload[] = {4};
XBee xbees[XBEE_NUM];
Rx16Response rx16s[XBEE_NUM];

//Variables to be used
int rssi;
byte cur_rssi[XBEE_NUM] = {0,0,0};
bool isMotion =false;
long ave =0,time;
int rssi_max[3] = {0,0,0},rssi_min[3];
int32_t rssi_time[3] = {0,0,0};

//Main Loop

void setup()
{
  /* add setup code here */
	//Initialize Arduino Serial Ports
	Serial.begin(115200);
	Serial1.begin(57600);
	Serial2.begin(57600);
	Serial3.begin(57600);
	//Initialize Xbees
	xbees[0].setSerial(Serial1);
	xbees[1].setSerial(Serial2);
	xbees[2].setSerial(Serial3);

	pinMode(LED_IND,OUTPUT);
	delay(500);
	time = millis();
}

void loop()
{
	int rssi_values[3];
	for(int i = 0; i<XBEE_NUM;i++)
	{
		rx16s[i] = Rx16Response();
		xbees[i].readPacket(READ_TIMEOUT);
		if (xbees[i].getResponse().isAvailable()) {
			if (xbees[i].getResponse().getApiId() == RX_16_RESPONSE) {
				xbees[i].getResponse().getRx16Response(rx16s[i]);
				rssi = rx16s[i].getRssi();
			#if MODE == BENCHMARK
				if(millis() - time < 10000)
				{
					rssi_max[i]++;
					Serial.print(rssi_max[i]);
					Serial.print(" ");
				}
			#elif MODE == RSSI
				Serial.write(rssi);
				//Serial.print(" ");
				cur_rssi[i] = rssi;

			#elif MODE == TIME
				Serial.print(millis() - rssi_time[i]);
				rssi_time[i] = millis();
				Serial.print(" ");
			#elif MODE == RSSI_TIME
				Serial.print(rssi);
				Serial.print(" ");
				Serial.print(millis() - rssi_time[i]);
				Serial.print("|");
				rssi_time[i] = millis();
				cur_rssi[i] = rssi;
				Serial.print(" ");
			#elif MODE == SINGLE
				if(i==1)	
				{
					Serial.write(rssi);
					cur_rssi[i] = rssi;
				}
			#endif // MODE == BENCHMARK
			}
		} else Serial.write(cur_rssi[i]);
		delay(XBEE_INTERVAL);

	}
	
#if MODE == SINGLE

#endif // MODE == SINGLE
	//Serial.println();
}

void collectData()
{
	
	
}
