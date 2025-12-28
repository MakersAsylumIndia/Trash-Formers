from ultralytics import YOLO
from PIL import Image
import subprocess
import time
import os

MODEL_PATH = "models/my_model.pt"
IMAGE_PATH = "images/test_capture.jpg"

os.makedirs("images", exist_ok=True)

model = YOLO(MODEL_PATH)

print("Capturing image...")
subprocess.run([
    "rpicam-still",
    "-o", IMAGE_PATH,
    "--width", "640",
    "--height", "480",
    "--nopreview"
])

img = Image.open(IMAGE_PATH)

print("Running detection...")
results = model(img, conf=0.5)
r = results[0]

if len(r.boxes) == 0:
    print("No objects detected")
else:
    for box in r.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        name = model.names[cls]
        print(f"Detected {name} (conf {conf:.2f})")
