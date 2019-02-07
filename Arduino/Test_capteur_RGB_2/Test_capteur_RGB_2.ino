const int s0=10;
const int s1=9;
const int s2=12;
const int s3=11;
const int out=8;

int dataR=0;
int dataG=0;
int dataB=0;

int offsetRed = 30;
int offsetGreen = 16;
int offsetBlue = 24;

void setup() 
{
   pinMode(s0,OUTPUT);
   pinMode(s1,OUTPUT);
   pinMode(s2,OUTPUT);
   pinMode(s3,OUTPUT);
   pinMode(out,INPUT);

   Serial.begin(9600);
   
  // Fréquence
   digitalWrite(s0,HIGH);
   digitalWrite(s1,HIGH);
   
}

void loop()
{
/*********************** calibrage Rouge ************************/
   digitalWrite(s2,LOW);
   digitalWrite(s3,LOW);

   dataR=pulseIn(out,LOW);
   delay(10);
/*********************** calibrage Vert ************************/
   digitalWrite(s2,LOW);
   digitalWrite(s3,HIGH);
   
   dataG=pulseIn(out,LOW);
   
   delay(10);
/*********************** calibrage Bleu ************************/

   digitalWrite(s2,HIGH);
   digitalWrite(s3,HIGH);
   
   dataB=pulseIn(out,LOW);
   
   delay(10);


  Serial.println(String(dataR) + " " + String(dataG) + " " + String(dataB));

   
   delay(2000);
}
