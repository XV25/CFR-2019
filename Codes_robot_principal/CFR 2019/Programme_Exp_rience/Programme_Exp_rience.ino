long unsigned currentMillis =0;
long unsigned currentMillis2 =0;
unsigned long previousMillis1 =0;
 
 
 /* Inclut la lib Servo pour manipuler le servomoteur */
#include <Servo.h>


/* Créer un objet Servo pour contrôler le servomoteur */
Servo monServomoteur;


int LED_bleu = 12;

int LED_rouge = 13;

int LED_verte_1 = 9;
int LED_verte_2 = 10;
int LED_verte_3 = 11;

int Moteur = 8;

bool rep = false;

const byte trig = 2;
const byte echo = 3;
/* Constantes pour le timeout */
const unsigned long MEASURE_TIMEOUT = 25000UL; // 25ms = ~8m à 340m/s

/* Vitesse du son dans l'air en mm/us */
const float SOUND_SPEED = 340.0 / 1000;


void waitOk(){

  int distance_fin = 0;

  while (distance_fin < 500){
    delay(1000);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    long measure = pulseIn(echo, HIGH, MEASURE_TIMEOUT);
    float distance_mm = measure / 2.0 * SOUND_SPEED;
    distance_fin = int(distance_mm);
    Serial.println(distance_fin);
  }
  
  
}

void setup() {
  
  Serial.begin(9600);
  
  // put your setup code here, to run once:

 pinMode(LED_bleu,OUTPUT);

 pinMode(LED_rouge,OUTPUT);

 pinMode(LED_verte_1,OUTPUT);
 pinMode(LED_verte_2,OUTPUT);
 pinMode(LED_verte_3,OUTPUT);

 
 // Juste pour avoir une sortie qui alimente le servomoteur 
 pinMode(7,OUTPUT);
 pinMode(6,OUTPUT);
 pinMode(5,OUTPUT); 
 pinMode(4,OUTPUT);
 pinMode(3,OUTPUT);

 digitalWrite(7,HIGH);
 digitalWrite(6,HIGH);
 digitalWrite(5,HIGH);
 digitalWrite(4,HIGH);
 digitalWrite(3,HIGH);


 

 digitalWrite(LED_bleu,LOW);

 digitalWrite(LED_rouge,LOW); 
 
 digitalWrite(LED_verte_1,LOW);
 digitalWrite(LED_verte_2,LOW);
 digitalWrite(LED_verte_3,LOW);


 pinMode(trig,OUTPUT);

 digitalWrite(trig,LOW);
 pinMode(echo,INPUT);
 waitOk();

 monServomoteur.attach(Moteur);

 

}

void Disco() {
  // Programme pour faire clignoter les leds...
  Disco_1();
  Disco_2();

}

void Disco_1() {
  // Programme pour faire clignoter les leds rouges et bleus
  
  digitalWrite(LED_bleu,HIGH);
  digitalWrite(LED_rouge,LOW);
  delay(200);
  
  digitalWrite(LED_rouge,HIGH);
  digitalWrite(LED_bleu,LOW);
  delay(200);
   
  }


void Disco_2() {
  // Programme pour faire clignoter les leds vertes
  
  digitalWrite(LED_verte_1,HIGH);
  digitalWrite(LED_verte_2,LOW);
  digitalWrite(LED_verte_3,LOW);
  delay(100);

  digitalWrite(LED_verte_1,LOW);
  digitalWrite(LED_verte_2,HIGH);
  digitalWrite(LED_verte_3,LOW);
  delay(100);

  digitalWrite(LED_verte_1,LOW);
  digitalWrite(LED_verte_2,LOW);
  digitalWrite(LED_verte_3,HIGH);
  delay(100);
  
  }
void moteur() {

  
 //if (rep == false){
  
//  for (int position = 89; position >= 75; position-- ) {
//    monServomoteur.write(position);
//    Serial.println(position);
//    delay(500);
//    }
//    rep = true;
// }

 
  monServomoteur.write(92);
 
  }


void loop() {
  // put your main code here, to run repeatedly:



Disco();

//monServomoteur.write(91);

currentMillis = millis();
while(rep == false and (millis()- currentMillis)<25000){

Disco();
monServomoteur.write(91);

}

rep = true;

monServomoteur.write(94);



  
//monServomoteur.write(90); 
}
