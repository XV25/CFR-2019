
int s=119;
//---------------------------------------------Variables moteurs----------------------------------------------//
const int 
PWM_A   = 3,
DIR_A   = 12,
BRAKE_A = 9,
PWM_B   = 11,
DIR_B   = 13,
BRAKE_B = 8,
SNS_A   = A0;
float pwm_right=0;
float pwm_left=0;
//on met le moteur en wait()
int inByte='w';
//--------------------------------------------------Variables codeurs--------------------------------------------------//
const byte pinEncodeur_right = 18;
const byte pinEncodeur_left = 20;
long posA_right=0;
long posA_left=0;
unsigned long timeDebutMesureVitesse=0;
long time_d;
long tempsMesure = 30; //temps entre chaque calcul de la vitesse
float vitesse_right = 0; //vitesse de rotation de la roue en rad par sec
float vitesse_left=0;
long compteurDebutMesureVitesse_right; //valeur du compteur au début de la mesure
long compteurDebutMesureVitesse_left;
float vmax=22;//A CHANGER!!!!!!!!!!!!!!!!!!!!!!!!!!!!! mesure expérimentale !!!!!!!!!!!!!!!!!!!!!!!!!!!
float resolution=300;
float distance=0;
long posdebutmesuredistance=0;
float angle=0;
float posdebutmesure_angle=0;
float vitesse_cons=15.0;
float vitesse_faible=14.0;
float vitesse_haute=16.0;
float d=0.026529;
float a=0.0166456;

long timeStart;

//---------------------------------------------------------------------FONCTIONS CODEUR ET REPERAGE -------------------------------------------------------------------//
void pos_right(){
  posA_right++;
}
void pos_left(){
  posA_left++;
}

void calculVitesse(){
  time_d=millis();
  if((time_d-timeDebutMesureVitesse)>=tempsMesure){
    vitesse_right = float(posA_right-compteurDebutMesureVitesse_right)*0.852/float(time_d-timeDebutMesureVitesse);
    vitesse_left = float(posA_left-compteurDebutMesureVitesse_left)/float(time_d-timeDebutMesureVitesse);
    timeDebutMesureVitesse = time_d;
    compteurDebutMesureVitesse_right = posA_right;
    compteurDebutMesureVitesse_left = posA_left;
  }  
}
void distance_parcouru(){ 
    distance=distance+(posA_left-posdebutmesuredistance)*d;
    posdebutmesuredistance=posA_left;
  }

void orientation_robot(){ // pour la fonction orientation on suppose que le robot va tourner sur lui même et inchallah c'est ce qui se passe 
  angle=angle+(posA_left-posdebutmesuredistance)*a;
  posdebutmesuredistance=posA_left;
}
void reset_constantes_de_distance(){// dans le script python je l'appellerai à chaque fin d'action pour pas saturer la mémoire (en effet j'ai créer plus de constantes que nécessaire)
  distance=0;
  posdebutmesuredistance=0;
  posA_right=0;
  posA_left=0;
  angle=0;
 }
//-----------------------------------------------------EQUILIBRAGE FONCTIONS MOTEUR-------------------------------------------------------------------//
void go(){
  digitalWrite(BRAKE_A, LOW);  // setting brake LOW disable motor brake
  digitalWrite(BRAKE_B, LOW);  // setting brake LOW disable motor brake
}

void wait(){
//  Serial.println("Wait\n");
  digitalWrite(BRAKE_A, HIGH);  // setting brake HIGH enable motor brake
  digitalWrite(BRAKE_B, HIGH);  // setting brake HIGH enable motor brake
  pwm_left=0;
  pwm_right=0;
  reset_constantes_de_distance();
}

void forward(float vitesse){
  go();
  digitalWrite(DIR_A, LOW);   // setting direction to LOW the motor will spin backward
  digitalWrite(DIR_B, HIGH);   // setting direction to HIGH the motor will spin forward
  pwm_right=pwm_right+0.05*float(vitesse-vitesse_right)*255/vmax;
  pwm_left=pwm_left+0.05*float(vitesse-vitesse_left)*255/vmax;
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
  analogWrite(PWM_B,(int)round(pwm_left));     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_A,(int)round(pwm_right)); 
  distance_parcouru();
}
void deplacer_droite(){
  go();
  digitalWrite(DIR_A, LOW);   // setting direction to LOW the motor will spin backward
  digitalWrite(DIR_B, HIGH);   // setting direction to HIGH the motor will spin forward
  pwm_right=pwm_right+0.05*float(vitesse_faible-vitesse_right)*255/vmax;
  pwm_left=pwm_left+0.05*float(vitesse_haute-vitesse_left)*255/vmax;
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
  analogWrite(PWM_B,(int)round(pwm_left));     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_A,(int)round(pwm_right) ); 
  distance_parcouru();
}

void deplacer_gauche(){
  go();
  digitalWrite(DIR_A, LOW);   // setting direction to LOW the motor will spin backward
  digitalWrite(DIR_B, HIGH);   // setting direction to HIGH the motor will spin forward
  pwm_right=pwm_right+0.05*float(vitesse_haute-vitesse_right)*255/vmax;
  pwm_left=pwm_left+0.05*float(vitesse_faible-vitesse_left)*255/vmax;
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
  analogWrite(PWM_B,(int)round(pwm_left));     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_A,(int)round(pwm_right)); 
  distance_parcouru();
}

void right(float vitesse){
  go();
  digitalWrite(DIR_A, HIGH);   // setting direction to HIGH the motor will spin forward
  digitalWrite(DIR_B, HIGH);   // setting direction to HIGH the motor will spin forward
  pwm_right=pwm_right+0.05*float(vitesse-vitesse_right)*255/vmax;
  pwm_left=pwm_left+0.05*float(vitesse-vitesse_left)*255/vmax;
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
  analogWrite(PWM_B,(int)round(0.5*pwm_left));     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_A,(int)round(0.5*pwm_right)); 
  orientation_robot();
  Serial.println(angle);
   
}

void left(float vitesse){
  go();
  digitalWrite(DIR_A, LOW);   // setting direction to LOW the motor will spin backward
  digitalWrite(DIR_B, LOW);   // setting direction to LOW the motor will spin backward
  pwm_right=pwm_right+0.05*float(vitesse-vitesse_right)*255/vmax;
  pwm_left=pwm_left+0.05*float(vitesse-vitesse_left)*255/vmax;
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
  analogWrite(PWM_B,(int)round(0.5*pwm_left));     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_A,(int)round(0.5*pwm_right));  
  orientation_robot();
  Serial.println(angle);
}

void apply_PWM(int b){
  switch (b){
    case 102 :        // "f"
      forward(vitesse_cons);
      break;
    case 108 :        // "l"
      left(vitesse_cons);
      break;
    case 114 :        // "r"
      right(vitesse_cons);
      break;
    case 111 :
      reset_constantes_de_distance(); // "o"
      break;
    case 119 :        // "w"
      wait();
      break;
    case 110 : //"n" neutre
      break;
    case 113 :         //q
      deplacer_gauche();
      break;
    case 100 :        //d
      deplacer_droite();
      break;
    default :
      wait();
  }
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
  attachInterrupt(digitalPinToInterrupt(pinEncodeur_right), pos_right , FALLING);
   pinMode(pinEncodeur_left,INPUT);
  attachInterrupt(digitalPinToInterrupt(pinEncodeur_left), pos_left , FALLING);

  //init vitesse
  compteurDebutMesureVitesse_right = posA_right;
  compteurDebutMesureVitesse_left = posA_left;
  timeDebutMesureVitesse = millis();

  timeStart = millis();
}

//---------------------------------------------------------------------------------------------------LOOP-----------------------------------------------------------------------------------------------------//
void loop() {
   calculVitesse();
     
  if (Serial.available()) {
       inByte = Serial.read();
       if(inByte == 97){
          Serial.print(distance);
       }else if (inByte != 10){
          s = inByte;
       }
  }
  if(millis()-timeStart < 4000){  
    s = 'f';
  }else if(millis()-timeStart < 5500){
    s = 'r';
  }else if(millis()-timeStart < 6800){
    s = 'f';
  }else if (millis() - timeStart < 7500){
    s = 'w';
  }
  apply_PWM(s);
  delay(50);  
  
}
