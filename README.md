# Purplle Store Intelligence

## Overview

Purplle Store Intelligence is a retail analytics platform that transforms customer movement and sales activity into actionable business insights. The system combines computer vision, customer journey tracking, footfall analytics, conversion funnel analysis, and sales intelligence to help store managers make data-driven decisions.

Built for the Purplle Tech Challenge.

---

## Features

### Customer Journey Tracking

* Track customer movement across store zones
* Reconstruct customer paths through the store
* Analyze engagement with different departments

### Footfall Analytics

* Monitor entries and exits
* Calculate real-time occupancy
* Identify peak traffic periods

### Revenue Intelligence

* Department-wise revenue analysis
* Revenue distribution across store zones
* Top-performing category identification

### Conversion Funnel Analysis

* Track customer progression from entry to purchase
* Identify drop-off points
* Measure conversion performance

### Business Insights Engine

* Automated store recommendations
* Peak sales hour detection
* Top-performing zone identification
* Salesperson performance analysis

---

## System Architecture

Video Cameras
→ YOLOv8 Person Detection
→ ByteTrack Tracking
→ Zone Mapping Engine
→ SQLite Database
→ FastAPI Backend
→ React Dashboard
→ Store Intelligence Insights

---

## Tech Stack

### Frontend

* React.js
* Recharts
* Framer Motion
* Axios

### Backend

* FastAPI
* Python

### Computer Vision

* YOLOv8
* ByteTrack
* OpenCV

### Database

* SQLite

### Deployment

* Vercel (Frontend)
* Render (Backend)

---

## Project Structure

```text
purplle-store-intelligence/
│
├── api/
│   ├── routes/
│   └── main.py
│
├── frontend/
│   ├── public/
│   └── src/
│
├── pipeline/
│
├── config/
│
├── data/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints

### Metrics

```http
GET /api/v1/metrics
```

### Insights

```http
GET /api/v1/insights
```

### Funnel

```http
GET /api/v1/funnel
```

### Customer Journey

```http
GET /api/v1/journey
```

### Health Check

```http
GET /health
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/agrima29/purplle-store-intelligence.git
cd purplle-store-intelligence
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn api.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### Run Frontend

```bash
cd frontend
npm install
npm start
```

Frontend URL:

```text
http://localhost:3000
```

---

## Live Demo

Frontend:
https://purplle-store-intelligence-three.vercel.app

Backend:
https://purplle-store-intelligence-dlca.onrender.com

---

## Business Impact

Purplle Store Intelligence enables:

* Better merchandising decisions
* Improved workforce allocation
* Enhanced customer journey visibility
* Higher conversion rates
* Data-driven retail operations

By converting raw customer movement and sales data into actionable recommendations, the platform helps retail managers optimize store performance and improve business outcomes.

---

## Author

Agrima Singh

B.Tech Computer Science

Built for the Purplle Tech Challenge.
