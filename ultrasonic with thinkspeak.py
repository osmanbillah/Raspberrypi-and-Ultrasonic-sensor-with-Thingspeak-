import RPi.GPIO as GPIO
import time
import requests

# ThingSpeak settings
THINGSPEAK_API_KEY = 'YOUR CHANNEL WRITE API_KEY'  # Replace with your Write API Key
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# GPIO pins
TRIG = 23
ECHO = 24

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.5)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

try:
    while True:
        dist = get_distance()
        print(f"Measured Distance: {dist} cm")

        # Send to ThingSpeak
        payload = {'api_key': THINGSPEAK_API_KEY, 'field1': dist}
        response = requests.get(THINGSPEAK_URL, params=payload)

        if response.status_code == 200:
            print("Data sent to ThingSpeak.")
        else:
            print("Failed to send data.")

        time.sleep(15)  # ThingSpeak allows one update every 15 seconds

except KeyboardInterrupt:
    print("Stopped by user.")
    GPIO.cleanup()

