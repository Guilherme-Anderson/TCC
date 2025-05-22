#include <Arduino.h>
#include <WiFi.h>
#include <Firebase_ESP_Client.h>
#include <FS.h>
#include <SPIFFS.h>

// Objetos Firebase
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Variáveis de configuração
String ssid, password, firebase_host, firebase_auth;
int ID = 0;

// Função para ler uma chave do arquivo config.env
String getEnvValue(String key) {
  File file = SPIFFS.open("/config.env", "r");
  if (!file) {
    Serial.println("Erro ao abrir config.env");
    return "";
  }

  while (file.available()) {
    String linha = file.readStringUntil('\n');
    linha.trim();  // Remove espaços e quebras de linha

    if (linha.startsWith("#") || linha.length() == 0) continue;

    int idx = linha.indexOf('=');
    if (idx != -1) {
      String k = linha.substring(0, idx);
      String v = linha.substring(idx + 1);
      k.trim();
      v.trim();

      if (k == key) {
        file.close();
        return v;
      }
    }
  }

  file.close();
  return "";
}


void setup() {
  Serial.begin(115200);

  // Inicializa SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("Erro ao montar SPIFFS");
    return;
  }

  // Carrega credenciais do arquivo
  ssid = getEnvValue("WIFI_SSID");
  password = getEnvValue("WIFI_PASSWORD");
  firebase_host = getEnvValue("FIREBASE_HOST");
  firebase_auth = getEnvValue("FIREBASE_AUTH");

  Serial.println("Valores carregados:");
  Serial.println("SSID: [" + ssid + "]");
  Serial.println("PASS: [" + password + "]");
  Serial.println("HOST: [" + firebase_host + "]");
  Serial.println("AUTH: [" + firebase_auth + "]");


  // Conecta ao Wi-Fi
  WiFi.begin(ssid.c_str(), password.c_str());
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado com IP: ");
  Serial.println(WiFi.localIP());

  // Configura Firebase
  config.database_url = firebase_host.c_str();
  config.signer.tokens.legacy_token = firebase_auth.c_str();

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  if (Firebase.ready()) {
    Serial.println("Firebase inicializado com sucesso!");
  } else {
    Serial.println("Falha ao inicializar o Firebase.");
  }
}

void loop() {
  int valor = random(0, 256);
  float tempo = millis() / 1000.0;
  ID++;

  String path = "/teste/" + String(millis());

  if (Firebase.RTDB.setInt(&fbdo, path + "/ID", ID) &&
      Firebase.RTDB.setFloat(&fbdo, path + "/tempo", tempo) &&
      Firebase.RTDB.setInt(&fbdo, path + "/valor", valor)) {
    Serial.println("Dados enviados com sucesso!");
  } else {
    Serial.println("Falha ao enviar dados:");
    Serial.println(fbdo.errorReason());
  }

  delay(5000);
}