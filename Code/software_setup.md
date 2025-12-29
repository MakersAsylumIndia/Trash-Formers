# Software Setup Guide — Smart Waste Sorting System

This guide explains how to set up the **Raspberry Pi software environment**, install dependencies, and run the project code.  
**Note:** This covers **software only** — hardware wiring is documented separately.

---
**Connecting to the Raspberry Pi**
1. Ensure that your computer and the Raspberry Pi are connected to the same network.
2. Find the IP address of the Raspberry Pi:
   ```bash
   arp -a
   ```
   Look for a device that matches the Raspberry Pi’s hostname or MAC address.
3. Connect to the Raspberry Pi using SSH:
   ```bash
   ssh pi@<PI_IP_ADDRESS>
   ```
**Update the Raspberry Pi**  
Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```
---

**Enable/Test the Camera**

Install the rpicam apps:
```bash
sudo apt install -y rpicam-apps
```
Verify camera is detected
```bash
rpicam-hello --list-cameras
```
Camera preview
```bash
rpicam-hello
```
Take a photo
```bash
rpicam-still -o test.jpg
```
If test.jpg is created, your camera is functioning correctly.

---

**Install System Packages**
Install the required system packages:
```bash
  sudo apt install -y
  sudo apt install python3-pip python3-venv
  sudo apt install python3-rpi.gpio
```

**Create a Python Virtual Environment**
Create and activate a virtual environment:
```bash
python3 -m venv yolo-env
source yolo-env/bin/activate
````
To exit the environment later:
```bash
deactivate
```

**Install Python Dependencies**
Upgrade pip and install the Python packages:
```bash
pip install ultralytics pillow RPi.GPIO
```
---

**Create Project Folders**
Create the necessary directories for models, images, and logs:
```bash
mkdir -p models images logs
```
Place your YOLO model in the models folder:
```bash
models/my_model.pt
```

**Run the Project**
Activate the virtual environment:
```bash
source yolo-env/bin/activate
```
Run the main program:
```bash
python smart_sort_detect.py
```
---
