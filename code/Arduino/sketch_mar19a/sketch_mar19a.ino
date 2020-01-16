int a=3;
void setup() {
  Serial.begin(9600);
  a=a*a;
  

}

void loop() {
  Serial.print(a);
}
