#include <SoftwareSerial.h>

#include <Cytron_SmartDriveDuo.h>

#include <Servo.h> 
#include <Stepper.h>
#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)



#define IN1 7 // Arduino pin 9 is connected to MDDS30 pin IN1.
#define AN1 3 // Arduino pin 6 is connected to MDDS30 pin AN1.
#define AN2 12 // Arduino pin 5 is connected to MDDS30 pin AN2.
#define IN2 13 // Arduino pin 8 is connected to MDDS30 pin IN2.
Cytron_SmartDriveDuo smartDriveDuo30(PWM_INDEPENDENT, IN1, IN2, AN1, AN2);
signed int speedLeft, speedRight;
signed int commande;
float Kp = 0.1;


const byte pinEncodeurALeft = 2;
const byte pinEncodeurBLeft = 4;

long odoLeft = 0;
unsigned long t0;
unsigned long t1;
long odo0;
long odo1;
float vitesse;
float er;
int r = 39;
long dt  = 50000;



const int stepsPerRevolution = 203;//203; //202 // change this to fit the number of steps per revolution
//float rapp_avancement = 11/60;  //ici, en mm/step 0.1833mm par step
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);//include <Stepper.h>


unsigned long tps;
// Declare the Servo pin 
int servoPin1 = 5; // servo pour monter / descendre le bras
int servoPin2 = 6; //servo pour serrer la pince
int tst = 0;
int k = 0;
Servo Servo1; 
Servo Servo2; 
double angle_preh = 0;
double angle_serr = 0;
double angle_ouv = 0;
double dist_ori = 0; // distance à laquelle le bras doit être placé initialement
float * p_cs; // contient le nombre de steps de déplacement par rapport à l'origine.

double angle_c_1 = 90;
double angle_c_2 = 90;
//char Instructions;
char Instructions[6];
size_t taille;
//String str_brs;
//String str_ang;
float arm_depl = 0;
float dist;





void apply_PWM(int b){
  switch (b){
    case 111 :
      odometer();     // "o"
      break;
    case 105:    //'i'
      ini();
      break;
    case 109://"m"
      motor();
      break;
    case 103: //"g"
      goldonium();
      break;
    case 112:
      palet();
      break;
    case 98: //"b"
      balance();
      break;
    case 99: //"c"
      pousse();
      break;
    case 100: //"d"
      retour();
      break;
    case 101: //"e"
      pousseBouton();
      break;
    default :
      nothing(b);
  }
}


void ini(){
  Serial.println("init");
}


void motor()
{
  speedLeft=-1;
  speedRight=0;
  int dirLeft = -1;
  int dirRight = 0;
  Serial.println("motor Commande gauche");
  
  ////////////transmission left ////////////////////////////////////////////
  while (dirLeft == -1)
  {
    if (Serial.available()){
      dirLeft = Serial.read();
    }
  }
  Serial.println(dirLeft);

  /*
  while (speedLeft == -1)
  {
    if (Serial.available()){
      speedLeft = Serial.read();
    }
  }
  */
  int lecture = -1;
  while (lecture != 0){
    lecture = -1;
    if (Serial.available()){
      lecture = Serial.read();
      Serial.println(lecture);
      speedLeft = speedLeft + lecture;
    }
  }
  speedLeft = speedLeft +1;
  if (dirLeft == 1)
  {
    speedLeft = -speedLeft;
  }
  Serial.println(speedLeft);
  t0 = micros();
  odo0 = odoLeft;
  //smartDriveDuo30.control(speedLeft, speedRight);

  
}


void encodeurTickALeft()
{
    if (digitalRead(pinEncodeurBLeft)!=0) {
      odoLeft--;
    }
    else {
      odoLeft++;
    }
}

void odometer(){
  Serial.println("arduino odometer Go");
  Serial.println(odoLeft);
}

//-------------------Nothing---------------------------------------------------------
void nothing(int b){
}


//----------------------setup + loop --------------------------------------------------
void setup() {
  
  Serial.begin(9600);
  //Serial.println("Carte arduino base roulante :");

  pinMode(pinEncodeurALeft,INPUT_PULLUP);
  pinMode(pinEncodeurBLeft,INPUT_PULLUP);
  //digitalWrite(pinEncodeurALeft, HIGH); //turn pullup resistor on
  //digitalWrite(pinEncodeurBLeft, HIGH); //turn pullup resistor on
  attachInterrupt(0, encodeurTickALeft, FALLING);
  t0 = micros();
  odo0 = odoLeft;
  speedLeft = 0;


   // set the speed at 60 rpm:
  myStepper.setSpeed(70); // ou 60
  // initialize the serial port:
  analogReference(EXTERNAL);
  // We need to attach the servo to the used pin number 
  Servo1.attach(servoPin1); 
  Servo2.attach(servoPin2); 

}


void loop() {
  
  if (Serial.available()) {
    int inByte = Serial.read();
    //Serial.write(inByte);
    apply_PWM(inByte);
  }
 Servo1.write(angle_c_1);
 Servo2.write(angle_c_2);
  t1 = micros();
  if (t1 -t0 > dt){
    odo1 = odoLeft - odo0;
    vitesse = 1e6*odo1*2*PI*r/(1024*dt);
    er = speedLeft-vitesse;
    if (speedLeft> 0){
      commande = min(commande + int(er*Kp),250);
      commande = max(commande,65);
    }
    else if (speedLeft <0){
      commande = max(commande + int(er*Kp),-250);
      commande = min(commande,-70);
      
    }
    else{
      commande = 0;
    }
    smartDriveDuo30.control(commande, speedRight);
    odo0 = odoLeft;
    t0 = t1;
  }
}
