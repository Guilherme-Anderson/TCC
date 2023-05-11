/*
 * This ESP32 code is created by esp32io.com
 *
 * This ESP32 code is released in the public domain
 *
 * For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-mysql
 */

#include <WiFi.h>
#include <HTTPClient.h>

const char WIFI_SSID[] = "Quarto";
const char WIFI_PASSWORD[] = "guigu123";

String HOST_NAME = "http://192.168.3.184"; // change to your PC's IP address
String PATH_NAME   = "/teste.php";
String queryString = "?temperature=";
int leitura = 0;
int leitura2 = 0;
int leitura3= 0;

void setup() {
  Serial.begin(9600); 

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

}

void loop() {

  leitura =  1 + (rand() % 40);
  leitura2 =  1 + (rand() % 40);
  leitura3 =  1 + (rand() % 40);
  Serial.println(queryString+leitura);
  
  HTTPClient http;

  http.begin(HOST_NAME + PATH_NAME + "?&bancada=" + leitura + "&leitura1=" + leitura2 + "&leitura2=" + leitura3); //HTTP
  int httpCode = http.GET();

  // httpCode will be negative on error
  if(httpCode > 0) {
    // file found at server
    if(httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);
    } else {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    }
  } else {
    Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();

  delay(2000);
}
