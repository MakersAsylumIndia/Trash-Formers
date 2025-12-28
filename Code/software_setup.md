# Software Setup Guide — Smart Waste Sorting System

This guide explains how to set up the **Raspberry Pi software environment**, install dependencies, and run the project code.  
**Note:** This covers **software only** — hardware wiring is documented separately.

---

**1️⃣ Update the Raspberry Pi**  
Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

**2️⃣ Enable the Camera**
Run the Raspberry Pi configuration tool:
```bash
sudo raspi-config
```
Navigate to:
Interface Options → Camera → Enable
Then reboot the Pi:
```bash
sudo reboot
```

**3️⃣ Install System Packages**
Install the required system packages:
```bash
  sudo apt install -y \
  python3 python3-pip python3-venv \
  python3-rpi.gpio
```

**4️⃣ Create a Python Virtual Environment**
Create and activate a virtual environment:
```bash
python3 -m venv yolo-env
source yolo-env/bin/activate
````
To exit the environment later:
```bash
deactivate
```

**5️⃣ Install Python Dependencies**
Upgrade pip and install the Python packages:
```bash
pip install ultralytics pillow RPi.GPIO
```

**6️⃣ Create Project Folders**
Create the necessary directories for models, images, and logs:
```bash
mkdir -p models images logs
```
Place your YOLO model in the models folder:
```bash
models/my_model.pt
```

**7️⃣ Test the Camera**
Capture a test image to verify the camera works:
```bash
rpicam-still -o test.jpg
```
If test.jpg is created, your camera is functioning correctly.

**8️⃣ Run the Project**
Activate the virtual environment:
```bash
source yolo-env/bin/activate
```


Run the main program:
```bash
python smart_sort_detect.py
```
