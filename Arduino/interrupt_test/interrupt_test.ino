const byte chanB = 3;
const byte chanA = 2;
long num = 0;
char cmd = 'x';

void setup() {
  pinMode(chanB, INPUT);
  pinMode(chanA, INPUT);
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(chanA), increment, RISING);
}

void loop() {
  cmd = 'x';
  if (Serial.available()){
    cmd = Serial.read();
    }
  if (cmd == 's'){ //Set
    num = 0;
  }
  else if (cmd == 'r'){ //Read
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
