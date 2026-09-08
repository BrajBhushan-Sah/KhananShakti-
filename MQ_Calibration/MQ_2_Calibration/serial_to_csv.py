import csv
import time
import serial
from datetime import datetime
from pathlib import Path

SCRIPT_FOLDER = Path(__file__).resolve().parent
CSV_FILENAME = SCRIPT_FOLDER / "MQ2_verification.csv"

print("CSV location:", CSV_FILENAME)

# Change this to your ESP32 port
SERIAL_PORT = "COM4"

BAUD_RATE = 115200

ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    timeout=2
)

time.sleep(2)

print(f"Connected to {SERIAL_PORT}")
print(f"Saving readings to {CSV_FILENAME}")
print("Press Ctrl+C to stop recording.\n")

header_written = False

try:
    with open(CSV_FILENAME, mode="w", newline="") as file:
        writer = csv.writer(file)

        while True:
            raw_line = ser.readline()

            if not raw_line:
                continue

            line = raw_line.decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not line:
                continue

            print(line)

            values = line.split(",")

            # Detect the heading sent by ESP32
            if line.startswith("sample,time_ms"):
                writer.writerow(["computer_datetime"] + values)
                header_written = True
                file.flush()
                continue

            if not header_written:
                writer.writerow([
                    "computer_datetime",
                    "sample",
                    "time_ms",
                    "time_s",
                    "sensor",
                    "raw_adc",
                    "adc_voltage",
                    "module_voltage"
                ])
                header_written = True

            # Accept only valid data rows
            if len(values) == 7 and values[0].isdigit():
                computer_time = datetime.now().isoformat(
                    timespec="milliseconds"
                )

                writer.writerow([computer_time] + values)

                # Immediately save each row to disk
                file.flush()

except KeyboardInterrupt:
    print("\nRecording stopped by user.")

finally:
    ser.close()
    print("Serial port closed.")
    print(f"CSV saved as: {CSV_FILENAME}")