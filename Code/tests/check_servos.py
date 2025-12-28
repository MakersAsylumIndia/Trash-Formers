import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO_SWIPE = 17      # GPIO17
SERVO_MOVE = 27       # GPIO27

GPIO.setup(SERVO_SWIPE, GPIO.OUT)
GPIO.setup(SERVO_MOVE, GPIO.OUT)

servo1 = GPIO.PWM(SERVO_SWIPE, 50)
servo2 = GPIO.PWM(SERVO_MOVE, 50)

servo1.start(0)
servo2.start(0)

def set_angle_slow(servo, start_angle, end_angle, step=2, delay=0.05):
    """Moves servo gradually for smooth motion"""
    if end_angle > start_angle:
        angles = range(start_angle, end_angle + 1, step)
    else:
        angles = range(start_angle, end_angle - 1, -step)

    for angle in angles:
        duty = 2 + (angle / 18)
        servo.ChangeDutyCycle(duty)
        time.sleep(delay)

    servo.ChangeDutyCycle(0)


try:
    print("Smooth test — SWIPE servo (GPIO17)")
    set_angle_slow(servo1, 0, 180)
    time.sleep(1)
    set_angle_slow(servo1, 180, 0)
    time.sleep(1)

    print("\nSmooth test — MOVEMENT servo (GPIO27)")
    set_angle_slow(servo2, 0, 180)
    time.sleep(1)
    set_angle_slow(servo2, 180, 0)
    time.sleep(1)

except KeyboardInterrupt:
    print("Stopped")

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
