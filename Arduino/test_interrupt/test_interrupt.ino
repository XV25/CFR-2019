int pin = 2;
volatile int state = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pin), change, FALLING);
}

void loop() {
  delay(500);  
  Serial.print(digitalRead(pin));
  Serial.println(state);
}

void change(){
  state++;
}
