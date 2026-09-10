# KhananShakti — Autonomous Mine Safety & Rescue Rover

## 📌 Project Overview

KhananShakti is an autonomous mine safety and rescue rover designed to explore hazardous underground mine environments, detect obstacles and hazards, identify survivors, and provide a real-time visualization of the mine environment.

The project currently contains a Python-based simulation and live monitoring dashboard. The simulation architecture is designed so that simulated sensor data can later be replaced by real hardware inputs from an ESP32, LiDAR/ToF sensors, ultrasonic sensors, gas sensors, motors, and a camera/AI system.

---

## 🏗️ Current System Architecture

```text
                    ┌─────────────────────┐
                    │   Mine Environment  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   ToF / LiDAR Scan   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Mine Map       │
                    │  Free / Unknown /   │
                    │      Obstacle       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Frontier Detection  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    A* Path Planner  │
                    │   + Cost Map        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        Rover        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌─────────────────┐        ┌──────────────────┐
       │ Semantic Mapping│        │  Rover Telemetry  │
       │ Gas / Water /   │        │                  │
       │ Crack / Debris /│        │ rover_state.json │
       │ Survivor        │        └────────┬─────────┘
       └─────────────────┘                 │
                                           ▼
                                 ┌────────────────────┐
                                 │  Streamlit + Plotly│
                                 │  Live Dashboard    │
                                 └────────────────────┘