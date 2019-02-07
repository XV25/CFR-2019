#include <Servo.h>
Servo monServomoteur;

void setup() {

  // Attache le servomoteur à la broche D9
  monServomoteur.attach(2);
  Serial.begin(9600);
}

void loop() {
//
//  // Fait bouger le bras de 0° à 180°
//  for (int position = 0; position <= 180; position++) {
//    monServomoteur.write(position);
//    delay(2);
//  }
//  delay(2000);
//  // Fait bouger le bras de 180° à 10°
//  for (int position = 180; position >= 0; position--) {
//    monServomoteur.write(position);
//    delay(2);
//  }

  monServomoteur.write(0);
  delay(3000);
  monServomoteur.write(120);
  delay(5000);
 

}
