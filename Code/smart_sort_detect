"""
Integrated vision-based waste sorting system.

Components:
- YOLO object detection
- Ultrasonic object triggering
- Dual-servo actuation (movement + swipe)
- Raspberry Pi GPIO control

Status: Final-prototype
"""
import RPi.GPIO as GPIO
import time
import subprocess
from ultralytics import YOLO
from PIL import Image
import os

# ---------- GPIO SETUP ----------
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

SERVO1_PIN = 17   # Swipe
SERVO2_PIN = 27   # Movement

GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

servo1 = GPIO.PWM(SERVO1_PIN, 50)
servo2 = GPIO.PWM(SERVO2_PIN, 50)

servo1.start(0)
servo2.start(0)

# ---------- SERVO STATE ----------
servo1_angle = 0
servo2_angle = 0

# ---------- YOLO SETUP ----------
MODEL_PATH = "models/my_model.pt"
IMAGE_PATH = "images/capture.jpg"
RESULT_PATH = "images/capture_result.jpg"

model = YOLO(MODEL_PATH)

# ---------- PARAMETERS ----------
DISTANCE_THRESHOLD = 18
COOLDOWN_TIME = 5
CONFIDENCE_THRESHOLD = 0.5
CARDBOARD_CLASS_NAME = "cardboard"

os.makedirs("images", exist_ok=True)

print("Smart waste detection system started")
time.sleep(2)

# ---------- ULTRASONIC ----------
def measure_distance(timeout=0.02):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() - start_time > timeout:
            return None

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() - start_time > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * 17150, 2)

# ---------- BIN LOGIC ----------
def get_bin(class_id):
    PAPER_CLASSES = [0, 3]
    PLASTIC_CLASSES = [4]
    METAL_CLASSES = [2]

    if class_id in PAPER_CLASSES:
        return "PAPER / CARDBOARD BIN"
    elif class_id in PLASTIC_CLASSES:
        return "PLASTIC BIN"
    elif class_id in METAL_CLASSES:
        return "METAL BIN"
    return None

# ---------- SMOOTH SERVO ----------
def set_angle_smooth(servo, target_angle, servo_id, step=1, delay=0.05):
    global servo1_angle, servo2_angle

    current_angle = servo1_angle if servo_id == 1 else servo2_angle

    if target_angle > current_angle:
        angle_range = range(current_angle, target_angle + 1, step)
    else:
        angle_range = range(current_angle, target_angle - 1, -step)

    for angle in angle_range:
        duty = 2 + (angle / 18)
        servo.ChangeDutyCycle(duty)
        time.sleep(delay)

    servo.ChangeDutyCycle(0)

    if servo_id == 1:
        servo1_angle = target_angle
    else:
        servo2_angle = target_angle

# ---------- MAIN LOOP ----------
try:
    while True:
        distance = measure_distance()

        if distance is None:
            time.sleep(0.3)
            continue

        print(f"Distance: {distance} cm")

        if distance < DISTANCE_THRESHOLD:
            print("Object detected — capturing image")

            subprocess.run([
                "rpicam-still",
                "-o", IMAGE_PATH,
                "--width", "640",
                "--height", "480",
                "--nopreview"
            ])

            img = Image.open(IMAGE_PATH)
            results = model(img, conf=CONFIDENCE_THRESHOLD)
            r = results[0]

            if r.boxes is None or len(r.boxes) == 0:
                print("No detection")
            else:
                names = model.names
                best_box = max(r.boxes, key=lambda b: float(b.conf[0]))

                class_id = int(best_box.cls[0])
                class_name = names[class_id]
                bin_name = get_bin(class_id)

                print(f"Detected: {class_name} → {bin_name}")

                # ---- SERVO ACTION BASED ON BIN ----
                if bin_name == "PAPER / CARDBOARD BIN":
                    set_angle_smooth(servo2, 180, servo_id=2)
                    time.sleep(1)
                    set_angle_smooth(servo1, 90, servo_id=1)
                    time.sleep(1)
                    set_angle_smooth(servo1, 0, servo_id=1)
                    set_angle_smooth(servo2, 0, servo_id=2)

                elif bin_name == "PLASTIC BIN":
                    set_angle_smooth(servo2, 90, servo_id=2)
                    time.sleep(1)
                    set_angle_smooth(servo1, 90, servo_id=1)
                    time.sleep(1)
                    set_angle_smooth(servo1, 0, servo_id=1)
                    set_angle_smooth(servo2, 0, servo_id=2)

                elif bin_name == "METAL BIN":
                    set_angle_smooth(servo1, 90, servo_id=1)
                    time.sleep(1)
                    set_angle_smooth(servo1, 0, servo_id=1)

                annotated = r.plot()
                Image.fromarray(annotated).save(RESULT_PATH)

            print(f"Cooldown {COOLDOWN_TIME}s\n")
            time.sleep(COOLDOWN_TIME)

        time.sleep(0.3)

except KeyboardInterrupt:
    print("Stopping system")

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
