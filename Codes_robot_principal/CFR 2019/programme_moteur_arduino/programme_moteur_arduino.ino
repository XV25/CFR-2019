#include <SoftwareSerial.h>
int ledTest =10 ;


#include <Cytron_SmartDriveDuo.h>
#define IN1 9 // Arduino pin 4 is connected to MDDS30 pin IN1.
#define AN1 6 // Arduino pin 5 is connected to MDDS30 pin AN1.
#define AN2 5 // Arduino pin 6 is connected to MDDS30 pin AN2.
#define IN2 8 // Arduino pin 7 is connected to MDDS30 pin IN2.
Cytron_SmartDriveDuo smartDriveDuo30(PWM_INDEPENDENT, IN1, IN2, AN1, AN2);
signed int speedLeft, speedRight;


const byte pinEncodeurARight = 3;
const byte pinEncodeurBRight = 7;


const byte pinEncodeurALeft = 2;
const byte pinEncodeurBLeft = 4;

long odoRight = 0;
long odoLeft = 0;







void apply_PWM(int b){
  switch (b){
    case 122 :        // "z"
      ledOff();
      break;
    case 115 :        // "s"
      ledOn();
      break;
    case 111 :
      odometer();     // "o"
      break;
    case 109://"m"
      motor();
      break;
    default :
      nothing();
  }
}

//------------------Fonction test----------------------------------
void ledOn(){
  Serial.println("led on");
  digitalWrite(ledTest, HIGH);
}


void ledOff(){
  Serial.println("led off");
  digitalWrite(ledTest, LOW);
}

//-------------------Fonction Moteur ------------------------------


void motor()
{
  int speedLeft=-1;
  int speedRight=-1;
  int dirLeft = -1;
  int dirRight = -1;
  Serial.println("motor Commande");
  
  ////////////transmission left ////////////////////////////////////////////
  while (dirLeft == -1)
  {
    if (Serial.available()){
      dirLeft = Serial.read();
    }
  }
  Serial.println(dirLeft);
  while (speedLeft == -1)
  {
    if (Serial.available()){
      speedLeft = Serial.read();
    }
  }
  if (dirLeft == 1)
  {
    speedLeft = -speedLeft;
  }
  Serial.println(speedLeft);

  ////////////transmission Right//////////////////////////////////////////

  while (dirRight == -1)
  {
    if (Serial.available()){
      dirRight = Serial.read();
    }
  }
  Serial.println(dirRight);
  while (speedRight == -1)
  {
    if (Serial.available()){
      speedRight = Serial.read();
    }
  }
  if (dirRight == 1)
  {
    speedRight = -speedRight;
  }
  Serial.println(-speedRight);

  smartDriveDuo30.control(speedLeft, speedRight);

  
}
//------------------Fonction Odometre------------------------------------------------

void odometer(){
  Serial.println("arduino odometer Go");
  Serial.println(odoRight);
  Serial.println(odoLeft);
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


void encodeurTickALeft()
{
    if ((PIND&0x10)!=0) {
      odoLeft--;
    }
    else {
      odoLeft++;
    }
}






//-------------------Nothing---------------------------------------------------------
void nothing(){
  Serial.println("nothing\n");
}


//----------------------setup + loop --------------------------------------------------
void setup() {
  
  Serial.begin(9600);
  //Serial.println("Carte arduino base roulante :");
  pinMode(ledTest,OUTPUT);



  // initialisation des encodeurs
  pinMode(pinEncodeurARight,INPUT_PULLUP);
  pinMode(pinEncodeurBRight,INPUT_PULLUP);
  //digitalWrite(pinEncodeurARight, HIGH); //turn pullup resistor on
  //digitalWrite(pinEncodeurBRight, HIGH); //turn pullup resistor on
  attachInterrupt(1, encodeurTickARight, FALLING);

  pinMode(pinEncodeurALeft,INPUT_PULLUP);
  pinMode(pinEncodeurBLeft,INPUT_PULLUP);
  //digitalWrite(pinEncodeurALeft, HIGH); //turn pullup resistor on
  //digitalWrite(pinEncodeurBLeft, HIGH); //turn pullup resistor on
  attachInterrupt(0, encodeurTickALeft, FALLING);


}


void loop() {
  
  if (Serial.available()) {
    int inByte = Serial.read();
    //Serial.write(inByte);
    apply_PWM(inByte);
  }
}
