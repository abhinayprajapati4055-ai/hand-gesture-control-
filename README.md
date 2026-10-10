# Hand Gesture Control System 🖐️

A Python computer vision project that uses hand gestures to control a computer through a webcam.

## Features

* Cursor movement using hand gestures
* Scrolling using two fingers
* Left-click using a pinch gesture
* Right-click using a pinky-only gesture
* Drag-and-drop using a fist
* Media play/pause using an open palm
* Volume control using two-hand gestures

## Technologies

* Python
* OpenCV
* MediaPipe
* PyAutoGUI

## Requirements

* Windows computer
* Python
* Working webcam

## Installation

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install the required packages.

```powershell
python -m pip install -r requirements.txt
```

5. Start the application.

```powershell
python main.py
```

Press `Q` to close the webcam window.

## Safety

This application can move the mouse, click, drag, and control media volume. Test it carefully before using it for important work.

## Author

Created as my first Python computer vision project.
