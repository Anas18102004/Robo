# Jerry — Voice-Interactive Autonomous Vision Robot

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Hardware](https://img.shields.io/badge/Hardware-Raspberry_Pi_4-C51A4A?style=flat&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/)
[![Vision](https://img.shields.io/badge/Vision-OpenCV_4-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![Control](https://img.shields.io/badge/Actuation-GPIO_PWM-blue)](https://pypi.org/project/RPi.GPIO/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An integrated embedded robotics platform combining real-time optical computer vision, motor actuation, and web-based teleoperation on an edge Raspberry Pi 4 compute core.

---

## 1. Executive Summary & Purpose

Physical robotic agents operating in unstructured domestic or educational environments must reconcile multi-modal sensor inputs—optical video streams, directional navigation commands, and actuator control loops—under strict edge compute constraints.

**Jerry** is an autonomous mobile robot built on a Raspberry Pi 4 that integrates:
- Real-time video frame capture and streaming via OpenCV.
- Dual-channel DC motor propulsion using pulse-width modulation (PWM) via an L298N H-bridge driver.
- A responsive, low-latency browser teleoperation interface (`index.html`) for manual override and diagnostic steering.
- Hardware-in-the-loop audio feedback and visual indicators for operational state monitoring.

---

## 2. Hardware Architecture & Pinout Specification

```mermaid
flowchart LR
    subgraph Compute ["Compute Core"]
        RPi["Raspberry Pi 4<br>(Linux Ubuntu / Pi OS)"]
    end

    subgraph Power ["Power Distribution"]
        Battery["Li-ion Battery Pack<br>(12V Main + 5V Regulated)"]
    end

    subgraph Actuation ["Mobility & Actuation"]
        L298N["L298N H-Bridge Driver"]
        MotorL["Left DC Motor (Tracks/Wheels)"]
        MotorR["Right DC Motor (Tracks/Wheels)"]
    end

    subgraph Sensors ["Perception & Telemetry"]
        Cam["Camera Sensor Module (USB / CSI)"]
        WebUI["Web Teleoperation Client (Browser)"]
    end

    Battery -->|12V Logic & Motor| L298N
    Battery -->|5V USB-C| RPi
    RPi -->|BCM GPIO 17, 18, 22, 23| L298N
    RPi -->|PWM ENA: 27, ENB: 24 (1 kHz)| L298N
    L298N --> MotorL
    L298N --> MotorR
    Cam -->|Optical Video Stream| RPi
    WebUI <-->|HTTP / Flask REST & MJPEG| RPi
```

### GPIO Pin Mapping (Broadcom / BCM Mode)

| Motor Channel | Signal Pin | BCM GPIO | Physical Header Pin | Function |
| :--- | :---: | :---: | :---: | :--- |
| **Left Motor** | `IN1` | `GPIO 17` | Pin 11 | Forward Direction Logic |
| **Left Motor** | `IN2` | `GPIO 18` | Pin 12 | Reverse Direction Logic |
| **Left Motor** | `ENA` | `GPIO 27` | Pin 13 | Speed Control (1 kHz PWM) |
| **Right Motor** | `IN3` | `GPIO 22` | Pin 15 | Forward Direction Logic |
| **Right Motor** | `IN4` | `GPIO 23` | Pin 16 | Reverse Direction Logic |
| **Right Motor** | `ENB` | `GPIO 24` | Pin 18 | Speed Control (1 kHz PWM) |

---

## 3. Software Architecture & Control Loop

- **`main.py`:** Flask HTTP camera capture microservice. Initializes optical video capture (`cv2.VideoCapture(0)`), acquires uncompressed frames, and exposes `/capture` endpoint for streaming.
- **`servo.py`:** Edge motor control server utilizing `RPi.GPIO`. Implements continuous 1 kHz PWM frequency modulation to adjust differential drive velocity during forward, reverse, turning, and pivoting maneuvers.
- **`index.html`:** Lightweight single-page teleoperation dashboard featuring touch/mouse navigation pads, speed regulators, and camera telemetry feedback.

---

## 4. Repository Structure

```
Robo/
├── main.py                             # Camera video capture & streaming service
├── servo.py                            # GPIO PWM differential motor driver service
├── index.html                          # Web teleoperation interface & joystick
├── requirements.txt                    # Python dependencies (Flask, OpenCV)
├── .gitignore                          # Artifact exclusions
├── Battery Low.mp4                     # Telemetry audiovisual asset
├── LipSync.mp4                         # Conversational audiovisual asset
└── WhatsApp Video 2025-09-30...mp4     # Physical hardware prototype demonstration
```

---

## 5. Prerequisites & Hardware Setup

### Hardware Requirements
1. Raspberry Pi 4 Model B (2GB+ RAM).
2. L298N Dual H-Bridge Motor Driver Module.
3. 2x Geared DC Motors with chassis/wheels.
4. USB or CSI Camera Module (640x480 or 1280x720).
5. External power supply (e.g., 2S/3S Li-ion pack) with common ground to Raspberry Pi.

### Software Installation

```bash
# Clone the repository onto the Raspberry Pi
git clone https://github.com/Anas18102004/Robo.git
cd Robo

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package dependencies
pip install -r requirements.txt
```

---

## 6. Execution & Operating Instructions

### 1. Launch Camera Capture Service

```bash
python main.py
```
*Initializes optical video stream on `http://<pi-ip-address>:5000/capture`.*

### 2. Launch Motor Actuation Controller

```bash
sudo python servo.py
```
*(Requires `sudo` permissions on Linux for direct memory-mapped GPIO access).*

### 3. Open Teleoperation Dashboard

Open your web browser and navigate to `http://<pi-ip-address>:5000` to control movement and observe visual telemetry.

---

## 7. License & Citation

Distributed under the **MIT License**.

```bibtex
@software{africawala2025jerryrobot,
  author = {Africawala, Mohammad Anas},
  title = {Jerry: Autonomous Vision and Physical Actuation Robot},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Anas18102004/Robo}
}
```
