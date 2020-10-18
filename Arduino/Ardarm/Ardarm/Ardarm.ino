#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int const portpin = A0;
int portval;
int time_to_go = 0;

void setup() {
  // put your setup code here, to run once:
  lcd.begin(16, 2);

  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

}


int last_port_value = 0;
int sec = 0;

int delayer = 1000;
bool flasher = false;

void loop() {
  // put your main code here, to run repeatedly:

  portval = analogRead(portpin);


  if(!(portval < last_port_value+5 && portval > last_port_value-5)){
    time_to_go = map(portval, 0, 1023, 0, 3600);
    delayer = 1000;
  }
  
  last_port_value = portval;
 
  if(portval > 0){
    if(time_to_go < 0){
      delayer = 200;
      
      if(flasher){
        digitalWrite(7, HIGH);
        digitalWrite(8, HIGH);
        digitalWrite(9, HIGH);
        flasher = false;  
      }
      else{
        digitalWrite(7, LOW);
        digitalWrite(8, LOW);
        digitalWrite(9, LOW);
        flasher = true;
      }
      
      tone(6, 2000, 10);
      lcd.clear();
      lcd.print("Ardarm went of!");
      
    }
    else{
      int min = time_to_go/60;
      int sec = time_to_go%60;
      
      lcd.clear();
      lcd.print("Time to go: ");
      
      lcd.setCursor(0, 1);
      lcd.print("min ");
      lcd.print(min);
      
      lcd.print(" sec ");
      lcd.print(sec);
      
      time_to_go--;
    }
    
    
  }
  else{

      delayer = 1000;
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);

        
      lcd.clear();
      lcd.print("Welcome to");
      
      lcd.setCursor(0, 1);
      lcd.print("Ardarm");
  }

  

  delay(delayer);
  

}
