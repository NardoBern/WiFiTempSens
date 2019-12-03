
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFiUDP.h>

// Configurazione Wifi
const char* ssid = "TempSensNetwork";
const char* password = "0111198125121984";
// Configurazione del sensore
const char* sensId = "cucina";
const char* wakeUpMsg = "cucinaSveglia";
const char* sleepMsg = "cucinaDormi";
boolean wifiConnected = false;
// Configurazione del bus one-wire sul GPIO 2
#define ONE_WIRE_BUS 2

// Definizione variabili
IPAddress broadcastIp(10,0,1,1);
IPAddress remote;
IPAddress myIpAddr;
unsigned int localPort = 64123;
WiFiUDP UDP;
boolean udpConnected = false;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer per contenere i dati in ricezione

// Istanza del bus di comunicazione OneWire
OneWire oneWire(ONE_WIRE_BUS);

// Istanza del blocco di interfaccia verso il sensore di temperatura
DallasTemperature DS18B20(&oneWire);
char temperatureCString[6];
char temperatureFString[6];

// Istanza del webserver sulla porta 80
WiFiServer server(80);

// Funzione di setup
void setup() {
  // Inizializzazione porta seriale per scopi di debug
  Serial.begin(115200);
  delay(10);
// Inizializzazione connessione Wifi
wifiConnected = connectWifi();

// Impostazione porta UDP
  if(wifiConnected){
  udpConnected = connectUDP();
    if (udpConnected){
  
    }
  }
  DS18B20.begin(); // Avvio sensore di temperatura
  
}



// Funzione ricorsiva
void loop() {
  // Acquisizione temperatura
  getTemperature();
  
   // Controllo se la connessione Wifi e la porta UDP sono connesse
if(wifiConnected){
  if(udpConnected){
    Serial.println("");
    Serial.print("Aspetto la sveglia");
    getUDP();
    // Attendo il messaggio di sveglia
      if(String(packetBuffer) == wakeUpMsg) // Messaggio di sveglia ricevuto
      {
        while(String(packetBuffer) != sleepMsg) // Sino a quando non ricevo il messaggio di tornare a dormire
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
  // Se invece non sono connesso alla Wifi, allora attendo un secondo e provo a riconnettermi
else{
  delay(1000);
  Serial.println("");
  Serial.print("Provo a connettermi nuovamente alla WiFi...");
  // Inizializzazione connessione alla Wifi
  wifiConnected = connectWifi();

// Se connesso, allora configura la porta UDP
  if(wifiConnected){
  udpConnected = connectUDP();
    if (udpConnected){
  
    }
  }
}
   
}

// Funzione di ricezione dati da UDP
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


// connessione e configurazione della porta UDP
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
// Funzione di connessione alla Wifi
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

// Funzione di lettura della temperatura
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
