float tempsdebut=0;
String trace = "";
int s=119;
//---------------------------------------------Variables moteurs----------------------------------------------//
 
const int PWM_A = 3;
const int DIR_A = 12;
const int BRAKE_A = 9;
const int PWM_B = 11;
const int DIR_B = 13;
const int BRAKE_B = 8;
const int SNS_A = A0;

int DC = 255;
int new_pwm=DC;
int pwm_right=0;
int pwm_left=0;
//on met le moteur en wait()
int inByte='w';

//--------------------------------------------------Variables codeurs--------------------------------------------------//
const byte pinEncodeur_right = 18;
const byte pinEncodeur_left = 20;
long pos_right=0;
long pos_left=0;

unsigned long timeDebutMesureVitesse=0;
long time_d;
long tempsMesure = 30; //temps entre chaque calcul de la vitesse
float vitesse_right = 0; //vitesse de rotation de la roue en rad par sec
float vitesse_left=0;

float vmax_right=24;
float vmax_left=21;
int resolution=300;

float distance_forward=0;
float rayon_roue=3;
long posdebutmesuredistance_forward=0;
long posdebutmesuredistance_backward=0;
float distance_entre_roues= 25.5/2;
float angle=0;
float posdebutmesure_angle=0;
float vitesse_cons=14.0;
float constante_bullshit=1;

//---------------------------------------------------------------------FONCTIONS CODEUR ET REPERAGE -------------------------------------------------------------------//
void change_pos_right(){
  pos_right++;
}
void change_pos_left(){
  pos_left++;
}

void calculVitesse(){
  float cL = 0.8;
  float cR = 1.0;
  
  time_d=millis();
  if((time_d-timeDebutMesureVitesse)>=tempsMesure){    
    vitesse_right = cR*float(pos_right)/float(time_d-timeDebutMesureVitesse);
    vitesse_left = cL*float(pos_left)/float(time_d-timeDebutMesureVitesse);
    timeDebutMesureVitesse = time_d;
    pos_right = 0;
    pos_left = 0;
  }  
}

//-----------------------------------------------------EQUILIBRAGE FONCTIONS MOTEUR-------------------------------------------------------------------//
void go(){
  digitalWrite(BRAKE_A, LOW);  // setting brake LOW disable motor brake
  digitalWrite(BRAKE_B, LOW);  // setting brake LOW disable motor brake
}

void forward(float vitesse){
  go();
  digitalWrite(DIR_A, LOW);   // setting direction to LOW the motor will spin backward
  digitalWrite(DIR_B, HIGH);   // setting direction to HIGH the motor will spin forward
  pwm_right=(int)round(pwm_right+0.5*float(vitesse-vitesse_right)*255/vmax_right);
  pwm_left=(int)round(pwm_left+0.5*float(vitesse-vitesse_left)*255/vmax_left);
  if(pwm_left>255){
    pwm_left=255;
  }
  else if(pwm_left<0){
    pwm_left=0;
  }
   if(pwm_right>255){
    pwm_right=255;
  }
  else if(pwm_right<0){
    pwm_right=0;
  }
  analogWrite(PWM_B,pwm_left);     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_A,pwm_right);  
}

void wait(){
//  Serial.println("Wait\n");
  digitalWrite(BRAKE_A, HIGH);  // setting brake HIGH enable motor brake
  digitalWrite(BRAKE_B, HIGH);  // setting brake HIGH enable motor brake
}

//-----------------------------------------------------------SETUP------------------------------------------------------------//
void setup() {
    
  /* Initialise le port série */
  Serial.begin(9600);
   
  // Configure the A and B output
  pinMode(BRAKE_A, OUTPUT);  // Brake pin on channel A
  pinMode(DIR_A, OUTPUT);    // Direction pin on channel A
  pinMode(BRAKE_B, OUTPUT);  // Brake pin on channel B
  pinMode(DIR_B, OUTPUT);    // Direction pin on channel B
  
  digitalWrite(BRAKE_A, HIGH);  // setting brake HIGH enable motor brake
  digitalWrite(BRAKE_B, HIGH);  // setting brake HIGH enable motor brake
  
  //Initialise l'encodeur//
  pinMode(pinEncodeur_right,INPUT);
  attachInterrupt(digitalPinToInterrupt(pinEncodeur_right), change_pos_right , FALLING);
   pinMode(pinEncodeur_left,INPUT);
  attachInterrupt(digitalPinToInterrupt(pinEncodeur_left), change_pos_left , FALLING);

  //init vitesse
  pos_right = 0;
  pos_left = 0;
  timeDebutMesureVitesse = millis();
}

//---------------------------------------------------------------------------------------------------LOOP-----------------------------------------------------------------------------------------------------//
void loop() {
  if (Serial.available()) {
       inByte = Serial.read();
       if (inByte==10){
        inByte=s;
       }
  }
  s=inByte;
  switch(inByte){
    case 102:
      calculVitesse();
      if(abs(millis()-tempsdebut)>10){
        forward(vitesse_cons);  
        Serial.print(pwm_left);
        Serial.print("        ");
        Serial.print(pwm_right);
        Serial.print("        ");  
        Serial.print(vitesse_left);
        Serial.print("        ");
        Serial.print(vitesse_right);
        Serial.print("        ");
        Serial.print(pos_left);
        Serial.print("        ");
        Serial.println(pos_right);
        tempsdebut=millis();
      }
      break;
    case 119:
      wait();
    break;
    default:
      wait();
    }
      
}
