// Motor control pins
const int motorPin1 = 9;    // Motor pin 1
const int motorPin2 = 10;   // Motor pin 2
const int encoderPinA = 2;  // Encoder pin A
const int encoderPinB = 3;  // Encoder pin B

// Sensors control pins
int fsrPin = 0;     // the FSR and 10K pulldown are connected to a0
int fsrReading;     // the analog reading from the FSR resistor divider
int sliderPin = 1;     // the slider potentiometer is connected to a1 
int sliderReading;  // the analog reading from the slider potentiometer

// Speed control variables
int motorSpeed = 80; // Motor speed (0-255 range)
// 250 for 9V

// Motor truning clockwise of counter clockwise
bool isMotorRunningClockwise = false;
bool isMotorRunningCounterClockwise = false;

// Position variables
int initialMaximumPosition = 920; // Slider initial maximum position (real value: 934)
int initialMinimumPosition = 290; // Slider initial minimum position (real value: 270)
int holdValue = 910; // FSR value when holding instrument
int minPosition = initialMinimumPosition; // Slider maximum closing position without instrument 
int maxPosition = initialMaximumPosition;
int rangeMovement;
int newMaxPosition = initialMaximumPosition;
int newMinPosition = initialMinimumPosition;
int minHoldValue = 300;
bool holding = false;

// Serial read values
const int bufferSize = 5; // Number of characters in the received number + 1 for the null terminator
char receivedCharArray[bufferSize]; // Array to hold the received characters and null terminator
char receivedFloatArray[bufferSize]; 
int index = 0;

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(11, OUTPUT);
  Serial.begin(9600);
}

void loop() {
 
  // Readings of the FSR and Sliding sensors
  fsrReading = analogRead(fsrPin);  
  sliderReading = analogRead(sliderPin);
 
//  Serial.print("Analog reading slider= ");
  Serial.print(sliderReading);
  Serial.print(",");
//  Serial.print("Analog reading FSR= ");
  Serial.print(fsrReading);     // print the raw analog reading
  Serial.print("\n");
  //Serial.println("Please enter one of the following options: 'h' to hold, 'r' to reset, 1 for scissors, 2 for needle holder, 3 for forceps, 'o' for opening and 'c' for closing");

  // Keyboard control
  if (Serial.available()>0) {
    // Read the incoming data
    char receivedChar = Serial.read();

    while (receivedChar != '\n') {
      if ((index < bufferSize - 1) && (receivedChar >= 32 && receivedChar <= 126)) {
        
        receivedCharArray[index] = receivedChar;
        index++;
      }
      receivedChar = Serial.read();
    }

//    Serial.println(receivedCharArray);
    
    for (int i = 1; i < index ; i++){
      receivedFloatArray[i-1] = receivedCharArray[i];
    }
    
    float receivedFloatValue = atof(receivedFloatArray) / 10;
    
    // Use switch case to check the received character
    switch (receivedCharArray[0]) {

           case 'L':
              rotateMotorCounterClockwiseContinuous(receivedFloatValue);
              holding = false;
              break;

           case 'R':
              rotateMotorClockwiseContinuous(receivedFloatValue);
              holding = false;
              break;
      
           // Hold instrument in place
           case 'h' :
                holdInstrument();
                holding = false;
                break;
                
           // Reset to the start position
           case 'r' : 
                rotateMotorCounterClockwise(); 
                maxPosition = initialMaximumPosition;
                minPosition = initialMinimumPosition;
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                motorSpeed = 80;
                holding = false;
                break;  
           
           // Stop
           case 's' : 
                stopMotor();
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                holding = false;
                break;
                
           // Pressure on the instrument to close
           case 'c' : 
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                rotateMotorClockwise();
                holding = false;
                break; 

           // Release pressure on the instrument to open
           case 'o' : 
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                rotateMotorCounterClockwise();
                holding = false;
                break;   


           // Minimum position for instrument 1: scissors
           case '1' : 
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                maxPosition = 640; //real value: 642
                minPosition = 360; //real value: 326
                motorSpeed = 90;
                holdValue = 928;
                holding = true;
                if (sliderReading > maxPosition) {
                  rotateMotorClockwise();
                }
                else{
                  stopMotor();
                }
                break; 
                
           // Minimum position for instrument 2: needle holder
           case '2' : 
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                maxPosition = 550; //real value: 646
                minPosition = 400; //real value: 
                motorSpeed = 80;
                holdValue = 900;
                holding = true;
                if (sliderReading > maxPosition) {
                  rotateMotorClockwise();
                }
                else{
                  stopMotor();
                }
                
                break; 
                
           // Minimum position for instrument 3: forceps
           case '3' : 
                newMaxPosition = initialMaximumPosition;
                newMinPosition = initialMinimumPosition;
                //maxPosition = sliderReading;
                maxPosition = 420; // real reading: 394
                minPosition = 340; // real reading: 300
                motorSpeed = 80;
                holdValue = 900;
                holding = true;
                if (sliderReading > maxPosition) {
                  rotateMotorClockwise();
                }
                else{
                  stopMotor();
                }
                
                break; 
      }

      // Reset the index and character array for the next value
      index = 0;
      memset(receivedCharArray, 0, bufferSize);
      memset(receivedFloatArray, 0, bufferSize);
  }


//Maximum openning/closing limit
  bool reachedMax = sliderReading > maxPosition || sliderReading > newMaxPosition;
  bool reachedMin = sliderReading < minPosition || sliderReading < newMinPosition;
  if ((reachedMax && isMotorRunningCounterClockwise) || (reachedMin && isMotorRunningClockwise)){
    stopMotor();
  }

// Holding condition
  if ((isMotorRunningClockwise) && (fsrReading>holdValue)) {
    stopMotor(); 
  }

  if (holding == true) {
    if ((isMotorRunningClockwise) && (fsrReading>minHoldValue)) {
        stopMotor(); 
    }
  }
}

void rotateMotorClockwise() {
  digitalWrite(motorPin2, LOW);
  analogWrite(motorPin1, motorSpeed);  // Control motor speed using PWM
  isMotorRunningClockwise = true;
  isMotorRunningCounterClockwise = false;
}

void rotateMotorCounterClockwise() {
  digitalWrite(motorPin1, LOW);
  analogWrite(motorPin2, motorSpeed);  // Control motor speed using PWM
  isMotorRunningCounterClockwise = true;
  isMotorRunningClockwise = false;
}

int rotateMotorClockwiseContinuous(float triggerValue){
  rangeMovement = maxPosition - minPosition;
  if (triggerValue < 1){
    newMinPosition = minPosition + (rangeMovement*triggerValue);
//    Serial.println(minPosition);
//    Serial.println(newMinPosition);
    
    if (sliderReading > newMinPosition){
      digitalWrite(motorPin2, LOW);
      analogWrite(motorPin1, motorSpeed);  // Control motor speed using PWM  
      isMotorRunningClockwise = true;
      isMotorRunningCounterClockwise = false;
      return newMinPosition;
    }
  }
}

int rotateMotorCounterClockwiseContinuous(float triggerValue){
  rangeMovement = maxPosition - minPosition;
  if (triggerValue < 1){
    newMaxPosition = maxPosition - (rangeMovement*triggerValue);
//    Serial.println(maxPosition);
//    Serial.println(newMaxPosition);
    
    if (sliderReading < newMaxPosition){
      digitalWrite(motorPin1, LOW);
      analogWrite(motorPin2, motorSpeed);  // Control motor speed using PWM
      isMotorRunningCounterClockwise = true;
      isMotorRunningClockwise = false;
      return newMaxPosition;
    }
  }
}

void stopMotor() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
}

void holdInstrument(){
  if (fsrReading>holdValue) {
     stopMotor();
  }
  else{
    rotateMotorClockwise(); 
  }
}
