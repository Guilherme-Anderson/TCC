
#include "Servo.h"          // Inclui a Biblioteca Servo.h
 
Servo meuservo;             // Cria o objeto servo para programação
 
int angulo = 0;             // Ajusta o ângulo inicial do Servo
 
void setup() {
  Serial.begin(9600);
  meuservo.attach(8);       // Declara o pino do servo
}
 
void loop() {
  for (angulo = 110; angulo < 180; angulo += 10) { 
    Serial.println(angulo);    // Executa movimentos no sentido horário
    meuservo.write(angulo);                            // Altera sua velocidade de 10 em 10
    delay(2000);                                       // Cada velocidade funciona por 2 segundos
  }
  
  meuservo.write(90); 
  Serial.println(90);                                    // Para o servo motor
  delay(2000);                                         // Aguarda 2 segundos para continuar
 
  for (angulo = 70; angulo >= 0; angulo -= 10) { 
    Serial.println(angulo);         // Executa movimentos no sentido anti horário
    meuservo.write(angulo);                            // Executa o ângulo de 10 em 10 graus
    delay(2000);                                       // Cada velocidade funciona por 2 segundos
  }
 
  meuservo.write(90); 
  Serial.println(90);                                    // Para o servo motor
  delay(2000);                                         // Aguarda 2 segundos para continuar
}