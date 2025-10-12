#define SW_PIN 8  // Button connected between pin 8 and GND

int last_input_val = HIGH;
unsigned long lastChangeTime = 0;
const unsigned long debounceDelay = 20; // ms

void setup() {
  Serial.begin(9600);
  pinMode(SW_PIN, INPUT_PULLUP);

  Serial.println("READY");
}

void loop() {
  int input_val = digitalRead(SW_PIN);
  unsigned long now = millis();

  if (input_val != last_input_val && (now - lastChangeTime) > debounceDelay) {
    last_input_val = input_val;
    lastChangeTime = now;

    if (input_val == LOW) {
      Serial.println("KEY_DOWN");
    } else {
      Serial.println("KEY_UP");
    }
  }
}