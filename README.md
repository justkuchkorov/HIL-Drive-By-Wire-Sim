# HIL Drive-by-Wire Control System (Python + CODESYS)

## Overview
This project demonstrates a **Hardware-in-the-Loop (HIL)** control system for an electronic throttle. It integrates a physical steering wheel, a Python-based simulation, and an industrial SoftPLC (CODESYS) communicating via Modbus TCP/IP.

## System Architecture
* **Input:** Thrustmaster T80 Racing Wheel (USB)
* **Plant Simulation:** Python 3.11 (Pygame + Matplotlib)
* **Controller:** CODESYS V3 SoftPLC (running IEC 61131-3 Logic)
* **Communication:** Modbus TCP (Real-time data exchange)

## Features
* **Real-Time Graphing:** Visualizes Pedal Input vs. Engine Output with <50ms latency.
* **Drive Modes:**
    * **SPORT Mode:** 1:1 throttle mapping (Direct response).
    * **ECO Mode:** Limits engine power to 50% for efficiency logic testing.
* **Safety Logic:** Auto-detects disconnected hardware and clamps signal values.

## How to Run
1.  Start the **CODESYS SoftPLC** and download the `DriveByWire_Controller.project`.
2.  Connect the Steering Wheel via USB.
3.  Run the Python script:
    ```bash
    pip install pymodbus pygame matplotlib
    python soup_graph_fixed.py
    ```

## Results
Below is the system response showing the controller intervention when switching from Sport to Eco mode while maintaining full throttle input.

![System Response Graph](/Docs/screenshot.png)
