# Glitch-Videos (Otomad Slit-Scan Generator)

A Python script for creating custom Otomad/YTPMV video effects using a heavy pixel-stretching slit-scan glitch.

Works on: **Windows**, **Linux**, and Android via **Termux + Termux:X11**.

## Requirements (Required Libraries)
* **`tkinter`** — Graphic User Interface (GUI)
* **`moviepy`** — Video processing and rendering
* **`numpy`** — High-performance matrix calculations for glitch effects
* **`threading`** — Multi-threading to prevent GUI freezing
* **`os`** — System navigation and file checking
* **`datetime`** — Generating unique timestamps for output files
* **`pathlib`** — Modern file path handling

---

## Installation & Launch via Termux (Android)

### 1. Preparing Termux Environment
First, make sure you download **Termux** and **Termux:X11** from trusted sources like **F-Droid** or **GitHub** (Do not use the Google Play Store version).

Open Termux and run the following commands to grant storage access and update packages:
```bash
termux-setup-storage
pkg update && pkg upgrade -y

2. Installing X11 Repository and Python
Set up the necessary graphic repositories and install Python:
pkg install x11-repo -y
pkg install termux-x11-nightly -y
pkg install python python-tkinter ffmpeg -y
pip install moviepy numpy


3. Running the App
⚠️ Important Note: For the script to easily find your files, make sure your input videos are placed inside your device's Downloads folder.
Navigate to your project directory, start the X11 server, and run the script:
cd /storage/emulated/0/Download/glich-vidoas/
termux-x11 :1 &
export DISPLAY=:1
python3 app.py

How to Use
Open the Termux:X11 application on your phone.
A language selection window will pop up. Choose either English or Русский and click OK / START.
In the main menu, click the BROWSE... (ОБЗОР...) button.
Select your video from the custom file manager.
Click the green GENERATE GLITCH (ГЕНЕРИРОВАТЬ ГЛИЧ) button and wait for the processing to finish.
Once a success window pops up, click OK.
Your newly created glitch video will be saved in your main downloads directory: /storage/emulated/0/Download/
