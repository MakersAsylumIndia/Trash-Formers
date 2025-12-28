import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

time.sleep(2)
print("Ultrasonic test started")

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - start > 0.02:
            return None

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - start > 0.02:
            return None

    duration = pulse_end - pulse_start
    return round(duration * 17150, 2)

try:
    while True:
        d = measure_distance()
        if d is None:
            print("Timeout — no echo")
        else:
            print(f"Distance: {d} cm")

        time.sleep(0.3)

except KeyboardInterrupt:
    print("Stopped")

finally:
    GPIO.cleanup()
