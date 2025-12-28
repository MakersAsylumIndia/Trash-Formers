# Troubleshooting Guide

This guide covers common software-side issues with the Raspberry Pi, camera system, ultrasonic sensor, YOLO detection, and debugging steps for the Smart Waste Detection project.

---

## 1. Raspberry Pi Power Issues

### **Symptoms**
- Raspberry Pi reboots or freezes randomly  
- Camera fails intermittently  
- Servos behave unpredictably  
- Terminal shows voltage warnings  

### **Cause**
Power supply is unstable or not supplying enough current.

### **Project Rule**
For reliability, **use ONLY the official Raspberry Pi power adapter**.  
Third-party adapters frequently cause undervoltage and system instability.

### **Fix**
- Replace the adapter with the official Raspberry Pi power unit
- Avoid powering servos directly from the Pi 5V rail
- Keep a stable power connection at all times

---

## 2. Camera & Library Issues

### **Project Requirement**
This project uses **RPICAM only**  
Do **not** use OpenCV camera capture (`cv2.VideoCapture`) because:
- It conflicts with the RPi camera stack
- It may produce empty frames or latency issues

### **Allowed**
```bash
rpicam-still -o test.jpg
```
Not allowed
python
```bash
cv2.VideoCapture(0)
```
## 📷 Common Errors

### Camera Errors
- `Cannot open camera`
- `No cameras available`
- `libcamera error`

### Fix Checklist ✅

**Camera ribbon cable issue**
- [ ] Power off Pi
- [ ] Reseat ribbon cable on both ends
- [ ] Ensure metal contacts face the correct direction
- [ ] Avoid bending or twisting the cable

**Enable camera support**
```bash
sudo raspi-config
# Interface Options → Camera → Enable
sudo reboot
```

## 3. Cardboard Detection Logic (Important)

### Project Design Behavior
Cardboard is frequently part of the **background inside the bin**.  

To prevent false detections, the code applies this rule:

- If cardboard is detected together with another class, the system **ignores the cardboard prediction** and processes only the other object.

This ensures:

- Background cardboard does **not trigger movement**
- Only the **true object being dropped** is acted on

### Expected Behavior
- **If only cardboard appears** → cardboard/paper logic runs  
- **If cardboard + plastic detected** → plastic logic runs  
- **If cardboard + metal detected** → metal logic runs  

> This behavior is intentional and part of the classification logic.

## 4. Model Training Considerations

If detection accuracy drops, consider improving the training dataset:

- Add varied lighting conditions
- Include multiple material textures
- Use different angles and object distances

**Retraining helps with:**

- Plastic reflections
- Transparent objects
- Low-confidence predictions

## 5. Debugging Detection Output

To understand model predictions, print detection results:

```python
print(results[0].boxes.cls, results[0].boxes.conf)
```
This helps identify:

- Wrong class predictions
- Low confidence scores
- Misclassified items

## 6. Ultrasonic Sensor Issues

### Symptoms
- Random distance readings
- Timeout messages
- Detection does not trigger

### Fix Checklist ✅
- [ ] Confirm `TRIG` & `ECHO` pins match the code
- [ ] Ensure stable 5V + GND connections
- [ ] Keep wires short
- [ ] Avoid routing wires near servos
- [ ] Add a slight delay between measurements

## 7. Debugging Test Scripts

Run individual test files to isolate issues:

### Servo Test (slow motion)
```bash
python check_servos.py
```
### Ultrasonic Sensor Test
```bash
python test_ultrasonic.py
```
### Camera + Detection Test
```bash
python detect_image.py
```
These scripts help confirm each module works before running the full system.
