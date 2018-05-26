/*
* Ultrasonic Sensor HC-SR04 and Arduino 
*Recieving program
*/

// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;

// defines variables
long duration;
int distance, Pdistance;

void setup() {
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
Serial.begin(9600); // Starts the serial communication
}

void loop() {
Pdistance=distance;
Calc();
distance= duration*0.034/2;
if (Pdistance==distance || Pdistance==distance+1 || Pdistance==distance-1){
  Serial.print("Measured Distance:");
  Serial.println(distance);
  }
  delay(500);
}

void Calc(){
  duration=0;
  Trigger_US();
  while(digitalRead(echoPin)==HIGH);
  delay(2);
  Trigger_US();
  duration = pulseIn(echoPin,HIGH); 
  Serial.print("duration:");
  Serial.println(duration);
  delay(10);
}

void Trigger_US(){
  //fake trigger the US sensor
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
}

