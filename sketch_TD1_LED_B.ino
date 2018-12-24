const int pinPhotoresistance = 0;
int iLed = 0;
int Tpal = 0;
int Val;

unsigned long T0 = 0;
unsigned long T1;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(6, OUTPUT);

  Serial.println("Hello");

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(37, HIGH);
  Val = analogRead(pinPhotoresistance);
//  Serial.println(Val);

 
  while (iLed<1000){
      digitalWrite(36, HIGH);
      delayMicroseconds(iLed);
      digitalWrite(36, LOW);
      delayMicroseconds(1000- iLed);
      delay (1);
      iLed = iLed + 100;

  }
  
  T1 = millis();
  Serial.println(T1 - T0);
  T0 = T1;
  iLed = 0;

}
