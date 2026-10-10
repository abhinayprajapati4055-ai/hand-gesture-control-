# 🚀 AirControlAI — Hand Gesture Control

**Control your computer using hand gestures with Python and computer vision!**

AirControlAI is a Python-based project that uses your webcam to recognize hand gestures and perform computer actions. The goal is to make computer interaction more intuitive, touch-free, and accessible.

## ✨ Features

* 🖐️ **Hand Gesture Recognition** — Detect hand gestures using your webcam.
* 🖱️ **Cursor Control** — Move the mouse pointer using your index finger.
* 📜 **Scrolling** — Scroll through pages using supported hand gestures.
* 👆 **Click Actions** — Perform supported mouse actions using gestures.
* 🔊 **Volume Control** — Control system volume using supported gestures.
* 🎥 **Real-Time Detection** — Process hand movements through a live webcam feed.
* 🏷️ **Gesture Labels** — Display recognized gestures on the webcam window.

> Note: Available gestures depend on the implementation in the current version of the code.

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI

## 📂 Project Structure

```text
AirControlAI/
├── main.py
├── gesture.py
├── requirements.txt
├── README.md
└── .gitignore
```

*Your actual repository may contain additional files or a slightly different structure.*

## 💻 Requirements

* Windows, macOS, or Linux
* Python installed on your computer
* A working webcam
* Git

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/abhinayprajapati4055-ai/hand-gesture-control-.git
```

### 2. Open the project folder

```bash
cd hand-gesture-control-
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this command in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 5. Install dependencies

If your repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If you do not have one, install the required packages:

```bash
pip install opencv-python mediapipe pyautogui
```

**Important:** Use compatible package versions for your code. If MediaPipe or OpenCV produces an error, check the versions required by your implementation.

### 6. Run AirControlAI

```bash
python main.py
```

Allow webcam access if your operating system requests permission.

## 🎮 How to Use

1. Connect or enable your webcam.
2. Run `main.py`.
3. Position your hand where the webcam can see it clearly.
4. Perform a supported gesture.
5. Watch the on-screen gesture label and corresponding computer action.

Use the gestures implemented in `gesture.py` and `main.py`.

## 🔒 Safety and Privacy

* The application uses your webcam for hand gesture recognition.
* Review the source code before running it.
* Mouse and keyboard automation can affect open applications.
* Keep an easy way to stop the program available while testing.

## 🎯 Project Goals

AirControlAI is a learning project exploring computer vision, real-time gesture recognition, and hands-free computer interaction.

Future improvements may include:

* Better gesture recognition accuracy
* Customizable gesture mappings
* Improved cursor smoothing
* More accessibility features
* Additional computer controls

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome!

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## 👨‍💻 Author

**Abhinay Prajapati**

GitHub: [@abhinayprajapati4055-ai](https://github.com/abhinayprajapati4055-ai)

---

⭐ If you find this project interesting, consider giving the repository a star!
