#include <Keypad.h>
#include <Servo.h>
Servo servo_10;

const byte ROWS = 4; 
const byte COLS = 4; 
String incomingByte ;    


char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 4, 3, 2}; 

Keypad digicode = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){

  Serial.begin(9600);
    pinMode(12, OUTPUT);
  servo_10.attach(11, 500, 2500);

}
  
void loop(){
  char bouton = digicode.getKey();
  
  if (bouton){
    Serial.println(bouton);
  }

/*
    if (Serial.available() > 0) {
    incomingByte = Serial.readStringUntil('\n');

    if (incomingByte == "acces") {
      LED_accepter();
    }

    if (incomingByte == "accesrefuse") {
      LED_refuser();
    }

    if (incomingByte == "installateuractive") {
      mode_installateur_activer();
    }

    if (incomingByte == "installateurdesactive") {
    mode_installateur_desactiver();
    }

      if (incomingByte == "fermer") {
      porte_former();
    }
  }


*/
  
}
/*
void moteur(){
     servo_10.write(0);
    delay(700); // Wait for 700 millisecond(s)
}

void moteurfermer(){
     servo_10.write(90);
    delay(700); // Wait for 700 millisecond(s)
}


void porte_former(){
      digitalWrite(12, HIGH);
      delay(500);
      digitalWrite(12, LOW);
      moteurfermer();
}

void mode_installateur_activer(){
      digitalWrite(12, HIGH);
}

void mode_installateur_desactiver(){
      digitalWrite(12, LOW);
}

void LED_accepter(){
      digitalWrite(12, HIGH);
      delay(1000);
      digitalWrite(12, LOW);
      moteur();
}

void LED_refuser(){
      digitalWrite(12, HIGH);
      delay(500);
      digitalWrite(12, LOW);
      delay(500);
      digitalWrite(12, HIGH);
      delay(500);
      digitalWrite(12, LOW);
      delay(500);
      digitalWrite(12, HIGH);
      delay(500);
      digitalWrite(12, LOW);
}
*/