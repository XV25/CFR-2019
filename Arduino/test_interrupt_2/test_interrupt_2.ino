// pins for the encoder inputs
const int ENCODER_A = 18; 
const int PWM_A = 3;
const int DIR_A = 12;
const int BRAKE_A = 9;

const int ENCODER_B = 20;
const int PWM_B = 11;
const int DIR_B   = 13;
const int BRAKE_B = 8;
 
float multi_A = 1;
float multi_B = 1;
 
// variables to store the number of encoder pulses
// for each motor
volatile unsigned long Count_A = 0;
volatile unsigned long Count_B = 0;

long StartCount_A;
long StartCount_B;

long tempsDeMarche = 5000;
long timeDebutMarche = 0;

void go(){
  digitalWrite(BRAKE_A, LOW);  // setting brake LOW disable motor brake
  digitalWrite(BRAKE_B, LOW);  // setting brake LOW disable motor brake
}
void forward(int pwm){
  go();
  digitalWrite(DIR_A, LOW);   // setting direction to LOW the motor will spin backward
  digitalWrite(DIR_B, LOW);   // setting direction to HIGH the motor will spin forward
  analogWrite(PWM_A, pwm);     // Set the speed of the motor, 255 is the maximum value
  analogWrite(PWM_B, pwm);     // Set the speed of the motor, 255 is the maximum value
     
}

void wait(){
  Serial.println("Wait\n");
  digitalWrite(BRAKE_A, HIGH);  // setting brake HIGH enable motor brake
  digitalWrite(BRAKE_B, HIGH);  // setting brake HIGH enable motor brake
}
 
void setup() {
  pinMode(ENCODER_A, INPUT);
  pinMode(ENCODER_B, INPUT);

   // Configure the A and B output
  pinMode(BRAKE_A, OUTPUT);  // Brake pin on channel A
  pinMode(DIR_A, OUTPUT);    // Direction pin on channel A
  pinMode(BRAKE_B, OUTPUT);  // Brake pin on channel B
  pinMode(DIR_B, OUTPUT);    // Direction pin on channel B
  digitalWrite(BRAKE_A, HIGH);  // setting brake HIGH enable motor brake
  digitalWrite(BRAKE_B, HIGH);  // setting brake HIGH enable motor brake

  
  // initialize hardware interrupts
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), EncoderEvent_A, FALLING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_B), EncoderEvent_B, FALLING);
  
  Serial.begin(9600);
  timeDebutMarche = millis();
}
 
void loop() {
  if((millis()-timeDebutMarche) <= tempsDeMarche){
      forward(200);
  }else{
    wait();
    delay(10000);
  }
  Serial.print("Count A: ");
  Serial.println(Count_A);
  Serial.print("Count B: ");
  Serial.println(Count_B);
  Serial.println();
  delay(10);
}
 
// encoder event for the interrupt call
void EncoderEvent_A() {
  Count_A++;
}
 
// encoder event for the interrupt call
void EncoderEvent_B() {
  Count_B++;
}
