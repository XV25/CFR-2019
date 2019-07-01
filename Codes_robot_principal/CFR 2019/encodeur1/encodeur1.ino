#include <SoftwareSerial.h>


#include <Cytron_SmartDriveDuo.h>
#define IN1 9 // Arduino pin 9 is connected to MDDS30 pin IN1.
#define AN1 6 // Arduino pin 6 is connected to MDDS30 pin AN1.
#define AN2 5 // Arduino pin 5 is connected to MDDS30 pin AN2.
#define IN2 8 // Arduino pin 8 is connected to MDDS30 pin IN2.
Cytron_SmartDriveDuo smartDriveDuo30(PWM_INDEPENDENT, IN1, IN2, AN1, AN2);
signed int speedLeft, speedRight;
signed int commande;
float Kp = 0.1;

const byte pinEncodeurARight = 3;
const byte pinEncodeurBRight = 7;

long odoRight = 0;
unsigned long t0;
unsigned long t1;
long odo0;
long odo1;
float vitesse;
float er;
int r = 39;
long dt  = 50000;


void apply_PWM(int b){
  switch (b){
    case 111 :
      odometer();     // "o"
      break;
    case 109://"m"
      motor();
      break;
    case 105:    //'i'
      ini();
      break;
    default :
      nothing(b);
  }
}


void ini(){
  Serial.println("init");
}

//-------------------Fonction Moteur ------------------------------


void motor()
{
  speedLeft=0;
  speedRight=-1;
  int dirLeft = 0;
  int dirRight = -1;
  Serial.println("motor Commande");
  
  ////////////transmission Right//////////////////////////////////////////

  while (dirRight == -1)
  {
    if (Serial.available()){
      dirRight = Serial.read();
    }
  }
  Serial.println(dirRight);

  /*
  while (speedRight == -1)
  {
    if (Serial.available()){
      speedRight = Serial.read();
    }
  }
  */
  int lecture = -1;
  while (lecture != 0){
    lecture = -1;
    if (Serial.available()){
      lecture = Serial.read();
      Serial.println(lecture);
      speedRight = speedRight + lecture;
    }
  }
  speedRight = speedRight +1;
  if (dirRight == 1)
  {
    speedRight = -speedRight;
  }
  Serial.println(speedRight);
  t0 = micros();
  odo0 = odoRight;
  //smartDriveDuo30.control(speedLeft, speedRight);

  
}
//------------------Fonction Odometre------------------------------------------------

void odometer(){
  Serial.println("arduino odometer Go");
  Serial.println(odoRight);
}

void encodeurTickARight()
{
    if ((PIND&0x80)!=0) {
      odoRight++;
    }
    else {
      odoRight--;
    }
}


//-------------------Nothing---------------------------------------------------------
void nothing(int b){
}


//----------------------setup + loop --------------------------------------------------
void setup() {
  
  Serial.begin(9600);
  //Serial.println("Carte arduino base roulante :");

  // initialisation des encodeurs
  pinMode(pinEncodeurARight,INPUT_PULLUP);
  pinMode(pinEncodeurBRight,INPUT_PULLUP);
  //digitalWrite(pinEncodeurARight, HIGH); //turn pullup resistor on
  //digitalWrite(pinEncodeurBRight, HIGH); //turn pullup resistor on
  attachInterrupt(1, encodeurTickARight, FALLING);
  t0 = micros();
  odo0 = odoRight;
  speedRight = 0;
}


void loop() {
  
  if (Serial.available()) {
    int inByte = Serial.read();
    //Serial.write(inByte);
    apply_PWM(inByte);
  }
  t1 = micros();
  if (t1 -t0 > dt){
    odo1 = odoRight - odo0;
    vitesse = 1e6*odo1*2*PI*r/(1024*dt);
    er = speedRight-vitesse;
    if (speedRight> 0){
      commande = min(commande + int(er*Kp),250);
      commande = max(commande,65);
    }
    else if (speedRight <0 ){
      commande = max(commande + int(er*Kp),-250);
      commande = min(commande,-70);
    }
    else{
      commande = 0;
    }
    smartDriveDuo30.control(speedLeft, commande);
    odo0 = odoRight;
    t0 = t1;
  }
  
}
