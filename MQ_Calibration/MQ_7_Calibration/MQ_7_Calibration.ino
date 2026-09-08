/*
  Individual MQ sensor calibration logger
  Board: ESP32

  Voltage divider:
  MQ AO -> 10k resistor -> GPIO34
  GPIO34 -> 20k resistor -> GND
*/

const int MQ_PIN = 34;

// Change this before calibrating another sensor
const char* SENSOR_NAME = "MQ-7";

const float R_TOP = 10000.0;
const float R_BOTTOM = 20000.0;

const unsigned long SAMPLE_INTERVAL_MS = 1000;

unsigned long previousSampleTime = 0;
unsigned long sampleNumber = 0;

float readAverageRaw(int pin, int samples) {
  uint32_t total = 0;

  for (int i = 0; i < samples; i++) {
    total += analogRead(pin);
    delay(2);
  }

  return total / static_cast<float>(samples);
}

float readAverageMillivolts(int pin, int samples) {
  uint32_t total = 0;

  for (int i = 0; i < samples; i++) {
    total += analogReadMilliVolts(pin);
    delay(2);
  }

  return total / static_cast<float>(samples);
}

void setup() {
  Serial.begin(115200);
  delay(1500);

  analogReadResolution(12);
  analogSetPinAttenuation(MQ_PIN, ADC_11db);

  // CSV column headings
  Serial.println(
    "sample,time_ms,time_s,sensor,raw_adc,adc_voltage,module_voltage"
  );
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - previousSampleTime >= SAMPLE_INTERVAL_MS) {
    previousSampleTime = currentTime;
    sampleNumber++;

    // Average several readings to reduce noise
    float rawADC = readAverageRaw(MQ_PIN, 20);
    float adcMillivolts = readAverageMillivolts(MQ_PIN, 20);

    float adcVoltage = adcMillivolts / 1000.0;

    float dividerRatio =
      R_BOTTOM / (R_TOP + R_BOTTOM);

    float moduleVoltage =
      adcVoltage / dividerRatio;

    Serial.print(sampleNumber);
    Serial.print(",");

    Serial.print(currentTime);
    Serial.print(",");

    Serial.print(currentTime / 1000.0, 3);
    Serial.print(",");

    Serial.print(SENSOR_NAME);
    Serial.print(",");

    Serial.print(rawADC, 2);
    Serial.print(",");

    Serial.print(adcVoltage, 4);
    Serial.print(",");

    Serial.println(moduleVoltage, 4);
  }
}
