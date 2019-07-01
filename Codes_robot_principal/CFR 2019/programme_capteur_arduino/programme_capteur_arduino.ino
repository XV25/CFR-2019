#include <SoftwareSerial.h>


// nom : X_coteRobot_posSurLeCote
const byte TRIG_Avant_Droit = 26; // Broche TRIGGER
const byte ECHO_Avant_Droit = 28;    // Broche ECHO

const byte TRIG_Avant_Gauche = 35; // Broche TRIGGER
const byte ECHO_Avant_Gauche = 37;  // broche echo2

const byte TRIG_Droit_Avant = 39; // Broche TRIGGER
const byte ECHO_Droit_Avant = 41;  // broche echo2

const byte TRIG_Droit_Arriere = 27; // Broche TRIGGER
const byte ECHO_Droit_Arriere = 29;  // broche echo2

const byte TRIG_Arriere_Droit = 30; // Broche TRIGGER
const byte ECHO_Arriere_Droit = 32;  // broche echo2

const byte TRIG_Arriere_Gauche = 31; // Broche TRIGGER
const byte ECHO_Arriere_Gauche = 33;  // broche echo2

const byte TRIG_Gauche_Arriere = 22; // Broche TRIGGER
const byte ECHO_Gauche_Arriere = 24;  // broche echo2

const byte TRIG_Gauche_Avant = 23; // Broche TRIGGER
const byte ECHO_Gauche_Avant = 25;  // broche echo2

const byte TRIG_Avant_Haut = 38; // Broche TRIGGER
const byte ECHO_Avant_Haut = 40;  // broche echo2

const byte TRIG_Arriere_Haut = 43; 
const byte ECHO_Arriere_Haut = 45; 

const byte trigger[10] = {26,35,39,27,30,31,22,23,38,43};
const byte echo[10] = {28,37,41,29,32,33,24,25,40,45};


/* Constantes pour le timeout */
const unsigned long MEASURE_TIMEOUT = 25000UL; // 25ms = ~8m à 340m/s

/* Vitesse du son dans l'air en mm/us */
const float SOUND_SPEED = 340.0 / 1000;




void apply_PWM(int b){
  switch (b){
    case 102 :        // "f"
      ultrasonAvant();
      break;
    case 108 :        // "l"
      ultrasonGauche();
      break;
    case 114 :        // "r"
      ultrasonDroit();
      break;
    case 98 :        // "b"
      ultrasonArriere();
      break;
    case 111 :  //"o"
      ultrasonObstacle();
      break;
    case 112 : //"p"
      ultrasonArriereObstacle();
      break;
    case 105:    //'i'
      ini();
      break;
    default :
      nothing();
  }
}



void ini(){
  Serial.println("init");
}

//---------------Ultrason ---------------------------------------------------------------

void ultrasonAvant(){
  Serial.println("UltrasonAvant G/D");
  ultrason(TRIG_Avant_Gauche,TRIG_Avant_Droit,ECHO_Avant_Gauche,ECHO_Avant_Droit);
}

void ultrasonGauche(){
  Serial.println("UltrasonGauche Av/Ar");
  ultrason(TRIG_Gauche_Avant,TRIG_Gauche_Arriere,ECHO_Gauche_Avant,ECHO_Gauche_Arriere);
}

void ultrasonDroit(){
  Serial.println("UltrasonDroit Av/Ar");
  ultrason(TRIG_Droit_Avant,TRIG_Droit_Arriere,ECHO_Droit_Avant,ECHO_Droit_Arriere);
}
void ultrasonArriere(){
  Serial.println("UltrasonArriere G/D");
  ultrason(TRIG_Arriere_Gauche,TRIG_Arriere_Droit,ECHO_Arriere_Gauche,ECHO_Arriere_Droit);
}

void ultrasonObstacle(){
  Serial.println("Ultrason Avant haut");
  ultrason(TRIG_Avant_Haut, TRIG_Avant_Droit ,ECHO_Avant_Haut, ECHO_Avant_Droit);
}

void ultrasonArriereObstacle(){
  Serial.println("Ultrason Avant haut");
  ultrason(TRIG_Arriere_Haut, TRIG_Arriere_Droit ,ECHO_Arriere_Haut, ECHO_Arriere_Droit);
}


void ultrason(const byte Trig_u1, const byte Trig_u2, const byte Echo_u1, const byte Echo_u2){
  digitalWrite(Trig_u1, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig_u1, LOW);
  long measure = pulseIn(Echo_u1, HIGH, MEASURE_TIMEOUT);
  float distance_mm = measure / 2.0 * SOUND_SPEED;
  int distance_fin = int(distance_mm);
  Serial.println(distance_fin);

  delay(10);
  digitalWrite(Trig_u2, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig_u2, LOW);
  measure = pulseIn(Echo_u2, HIGH, MEASURE_TIMEOUT);
  distance_mm = measure / 2.0 * SOUND_SPEED;
  distance_fin = int(distance_mm);
  Serial.println(distance_fin);
}


void ultra(){

  Serial.println(" arduino ultrason ok");
 
  for (int i = 0; i<8; i++)
  {
    // 1. Lance une mesure de distance en envoyant une impulsion HIGH de 10µs sur la broche TRIGGER 
    digitalWrite(trigger[i], HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger[i], LOW);
    
    // 2. Mesure le temps entre l'envoi de l'impulsion ultrasonique et son écho (si il existe) 
 
    long measure = pulseIn(echo[i], HIGH, MEASURE_TIMEOUT);
     
    // 3. Calcul la distance à partir du temps mesuré 
    float distance_mm = measure / 2.0 * SOUND_SPEED;
    int distance_fin = int(distance_mm);
    // Affiche les résultats en mm, cm et m 
    Serial.println(distance_fin);
    delay(10);
  }
}



//-------------------Nothing---------------------------------------------------------
void nothing(){
  Serial.println("nothing\n");
}

//----------------------setup + loop --------------------------------------------------
void setup() {
  
  Serial.begin(9600);
  
  /* Initialise les broches */
  for (int i =0; i<10;i++)
  {
    pinMode(trigger[i], OUTPUT);
    digitalWrite(trigger[i], LOW); // La broche TRIGGER doit être à LOW au repos
    pinMode(echo[i], INPUT);
  }
  
}


void loop() {
  
  if (Serial.available()) {
    int inByte = Serial.read();
    apply_PWM(inByte);
  }
}
