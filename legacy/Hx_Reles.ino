#define STATIC (1) 

#include <UIPEthernet.h>
#include "HX711.h"

EthernetServer server = EthernetServer(1000); //ListenPort
HX711 scale(6,5);

void setup() {

  Serial.begin(57600);
  Serial.println("Teste");

  uint8_t mac[6] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

  if (STATIC) 
  {
    IPAddress myIP(192,168,1,42);
    Ethernet.begin(mac, myIP);
  }
  else
  {
    int gotIP = Ethernet.begin(mac);
    if (gotIP)
    {
      Serial.println("DHCP got IP");
    }
    else
    {
      Serial.println("DHCP failed");
    }
     
  }


  Serial.print("localIP: ");
  Serial.println(Ethernet.localIP());
  Serial.print("subnetMask: ");
  Serial.println(Ethernet.subnetMask());
  Serial.print("gatewayIP: ");
  Serial.println(Ethernet.gatewayIP());
  Serial.print("dnsServerIP: ");
  Serial.println(Ethernet.dnsServerIP());

  server.begin();

  // HX711 Setup
  int calibration_factor = 870;
  scale.set_scale(calibration_factor);
  scale.tare(255);// n must be less than 255
  delay(500);

  // Relay Setup
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  
}



void arm() {
  digitalWrite(8, HIGH);
}

void sup2() {
  digitalWrite(8, LOW);
}

void fire() {
  digitalWrite(9, HIGH);
}

void sup() {
  digitalWrite(9, LOW);
}




void loop() {

  if (EthernetClient client = server.available())
    {
      while(true)
      {
        Serial.print(scale.get_units());
        Serial.print(";");   
        Serial.println(millis());
        
        client.print(scale.get_units());
        client.print(";");   
        client.println(millis());

        if (client.available()) {
          String message = client.readString();
          if (message == "arm\r\n") {
            arm();
             }
          else if (message == "sup2\r\n") {
            sup2(); 
             }
          else if (message == "fire\r\n") {
            fire();      
             }
          else if (message == "sup\r\n") {
            sup();
            }
          }  
      }
    }
}
