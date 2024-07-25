/*Left_motor*/
#define DIR1  12
#define PWM1  11
/*right_motor*/
#define DIR2  10
#define PWM2  9
void setup() {
  pinMode(DIR1, OUTPUT);
  pinMode(DIR2, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);

}

void loop() {
  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, HIGH);
  analogWrite(PWM1, 200);
  analogWrite(PWM2, 200);

}
