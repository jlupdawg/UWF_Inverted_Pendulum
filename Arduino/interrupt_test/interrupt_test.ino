const byte chanB = 3;
const byte chanA = 2;
volatile byte state = LOW;
unsigned long num = 0;

void setup() {
  pinMode(chanB, INPUT);
  pinMode(chanA, INPUT);
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(chanA), increment, RISING);
}

void loop() {
  if (Serial.available() > 0 && Serial.read() == 'r'){
    Serial.println(num);
  }
}

void increment() {
  if (digitalRead(chanB) == 0){
    num++;
  }
  else{
    num--;
  }
}
