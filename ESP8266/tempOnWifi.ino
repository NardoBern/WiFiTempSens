// Including the ESP8266 WiFi library
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFiUDP.h>

// Replace with your network details
const char* ssid = "TempSensNetwork";
const char* password = "0111198125121984";
const char* sensId = "cucina";
const char* wakeUpMsg = "cucinaSveglia";
const char* sleepMsg = "cucinaDormi";
boolean wifiConnected = false;
// Data wire is plugged into pin D1 on the ESP8266 12-E - GPIO 2
#define ONE_WIRE_BUS 2

IPAddress broadcastIp(10,0,1,1);
IPAddress remote;
IPAddress myIpAddr;

// UDP variables
unsigned int localPort = 64123;
WiFiUDP UDP;
boolean udpConnected = false;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature DS18B20(&oneWire);
char temperatureCString[6];
char temperatureFString[6];

// Web Server on port 80
WiFiServer server(80);

// only runs once on boot
void setup() {
  // Initializing serial port for debugging purposes
  Serial.begin(115200);
  delay(10);
// Initialise wifi connection
wifiConnected = connectWifi();

// only proceed if wifi connection successful
  if(wifiConnected){
  udpConnected = connectUDP();
    if (udpConnected){
  
    }
  }
  DS18B20.begin(); // IC Default 9 bit. If you have troubles consider upping it 12. Ups the delay giving the IC more time to process the temperature measurement
  
}



// runs over and over again
void loop() {
  getTemperature();
  //Serial.println(temperatureCString);
  
   // check if the WiFi and UDP connections were successful
if(wifiConnected){
  if(udpConnected){
    Serial.println("");
    Serial.print("Aspetto la sveglia");
    getUDP();
    //Start broadcast of Temperature
      if(String(packetBuffer) == wakeUpMsg) //If start packet is received
      {
        while(String(packetBuffer) != sleepMsg) //Stops transmitting Temperature Data if "STOP" is received on UDP
        {
          getTemperature();
          memset(packetBuffer, 0, sizeof(packetBuffer));
          UDP.beginPacket(remote, 64123);
          Serial.println("");
          Serial.print("Invio il id sensore: ");
          Serial.print(sensId);
          UDP.write(sensId);
          UDP.endPacket();
          delay(100);
          getUDP();
          if (String(packetBuffer) == "GetTemp") {
              Serial.println("");
              Serial.print("Invio Temp. °C: ");
              Serial.print(temperatureCString);
              UDP.write(temperatureCString);
              UDP.endPacket();
              }
          else if (String(packetBuffer) == "GetAddr") {
              Serial.println("");
              Serial.print("Invio indirizzo IP: ");
              Serial.print(WiFi.localIP());
              //UDP.write(myIpAddr);
              //UDP.endPacket();
          }
          memset(packetBuffer, 0, sizeof(packetBuffer));  
          delay(100);
          getUDP();
          //Serial.println(String(packetBuffer));
        }
      }
    }
delay(10);   

  }
   
}

//Get UDP Data
void getUDP(){
  int packetSize = UDP.parsePacket();
  if(packetSize)
    {
      Serial.println("");
      Serial.print("Received packet of size ");
      Serial.println(packetSize);
      Serial.print("From ");
      //IPAddress remote = UDP.remoteIP();
      remote = UDP.remoteIP();
      for (int i =0; i < 4; i++)
        {
          Serial.print(remote[i], DEC);
          if (i < 3)
            {
              Serial.print(".");
            }
        }
      Serial.print(", port ");
      Serial.println(UDP.remotePort());
      
      // read the packet into packetBufffer
      UDP.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
      Serial.println("Contents:");
      Serial.print(packetBuffer);
    }
}


// connect to UDP – returns true if successful or false if not
boolean connectUDP()
{
  boolean state = false;

  Serial.println("");
  Serial.println("Connecting to UDP");

  if(UDP.begin(localPort) == 1)
    {
    Serial.println("Connection successful");
    state = true;
    }
  else
    {
    Serial.println("Connection failed");
    }

  return state;
}
// connect to wifi – returns true if successful or false if not
boolean connectWifi()
{
  boolean state = true;
  int i = 0;
  IPAddress ip(10,0,1,10);
  IPAddress subnet(255,0,0,0);
  IPAddress gateway(10,0,1,1);
  WiFi.config(ip, gateway, subnet);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("Connecting to WiFi");

  // Wait for connection
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
    if (i > 10)
      {
      state = false;
      break;
      }
    i++;
  }
  if (state)
    {
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    myIpAddr = WiFi.localIP();
    }
  else 
    {
    Serial.println("");
    Serial.println("Connection failed.");
    }
  return state;
}

//Get Temperature of 18D20
void getTemperature() 
{
  float tempC;
  float tempF;
  do {
    DS18B20.requestTemperatures(); 
    tempC = DS18B20.getTempCByIndex(0);
    dtostrf(tempC, 2, 2, temperatureCString);
    //Serial.println("");
    //Serial.print("Temp °C: ");
    //Serial.print(temperatureCString);
    tempF = DS18B20.getTempFByIndex(0);
    dtostrf(tempF, 3, 2, temperatureFString);
    delay(100);
  } while (tempC == 85.0 || tempC == (-127.0));
}
