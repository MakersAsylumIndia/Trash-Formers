# Software Setup Guide — Smart Waste Sorting System

This guide explains how to set up the **Raspberry Pi software environment**, install dependencies, and run the project code.  
**Note:** This covers **software only** — hardware wiring is documented separately.

---

## 1️⃣ Update the Raspberry Pi

Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
2️⃣ Enable the Camera
Run the Raspberry Pi configuration tool:
sudo raspi-config
Navigate to:
Interface Options → Camera → Enable
Then reboot the Pi:
sudo reboot
3️⃣ Install System Packages
Install required system packages:
sudo apt install -y \
  python3 python3-pip python3-venv \
  python3-opencv \
  libatlas-base-dev libopenblas-dev \
  libjpeg-dev libtiff5
4️⃣ Create a Python Virtual Environment
Create and activate a virtual environment:
python3 -m venv yolo-env
source yolo-env/bin/activate
To exit the environment later:
deactivate
5️⃣ Install Python Dependencies
Upgrade pip and install Python packages:
pip install --upgrade pip
pip install ultralytics pillow RPi.GPIO opencv-python
6️⃣ Create Project Folders
Create necessary directories for models, images, and logs:
mkdir -p models images logs
Place your YOLO model in the models folder, for example:
models/my_model.pt
7️⃣ Test the Camera
Capture a test image to verify the camera works:
rpicam-still -o test.jpg

8️⃣ Run the Project
Activate the environment:
source yolo-env/bin/activate

Run the program:
python smart_sort_detect.py
