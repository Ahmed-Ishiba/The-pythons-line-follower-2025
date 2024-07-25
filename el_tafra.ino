#define left_tafra_pwm_1 6
#define left_tafra_pwm_2 9
//#define right_tafra_pwm_1 10
//#define right_tafra_pwm_2 11
void setup() {
  pinMode(left_tafra_pwm_1, OUTPUT);
  pinMode(left_tafra_pwm_2, OUTPUT);
//  pinMode(right_tafra_pwm_1, OUTPUT);
//  pinMode(right_tafra_pwm_2, OUTPUT);
}

void loop() {
  digitalWrite(left_tafra_pwm_1, LOW)
  analogWrite(left_tafra_pwm_2, 255)
//  digitalWrite(right_tafra_pwm_1, LOW)
//  analogWrite(right_tafra_pwm_2, 255)
}
