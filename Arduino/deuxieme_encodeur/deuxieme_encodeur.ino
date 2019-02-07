const byte pinEncodeur = 2;
long posA=0;
unsigned long timeDebutMesureVitesse=0;
long tempsMesure = 30;
float vitesse=0;
long compteurDebutMesureVitesse=0;
long tempsdebut=0;


void pos(){
  posA++;
}


void calculVitesse(){
  if((millis()-timeDebutMesureVitesse)>=tempsMesure){
    vitesse = float(posA-compteurDebutMesureVitesse)/float(millis()-timeDebutMesureVitesse);
    timeDebutMesureVitesse = millis();
    posA=0;
    compteurDebutMesureVitesse = posA;
  }
   
  }  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pinEncodeur,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinEncodeur), pos , FALLING);
  compteurDebutMesureVitesse = posA;
  timeDebutMesureVitesse = millis();
  tempsdebut=millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  calculVitesse();
  if(abs(millis()-tempsdebut)>1000){
   Serial.println(vitesse);
   tempsdebut=millis();
  }

}
