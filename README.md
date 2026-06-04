# Purplle Store Intelligence

### Transforming Store Activity into Actionable Business Insights

Purplle Store Intelligence is a retail analytics platform that combines computer vision, customer journey tracking, footfall analytics, conversion funnel analysis, and sales intelligence to help store managers make data-driven decisions.

Built for the **Purplle Tech Challenge 2026**.

---

## 🚀 Live Demo

### Frontend

https://purplle-store-intelligence-three.vercel.app

### Backend API

https://purplle-store-intelligence-dlca.onrender.com

### Source Code

https://github.com/agrima29/purplle-store-intelligence

---

## 🎯 Problem Statement

Retail stores generate large volumes of customer movement and sales data every day. However, store managers often lack visibility into:

* Customer movement patterns
* High-performing store zones
* Conversion bottlenecks
* Footfall trends
* Salesperson effectiveness
* Revenue-driving activities

This leads to:

* Missed revenue opportunities
* Inefficient staffing decisions
* Poor merchandising strategies
* Limited understanding of customer behavior

Purplle Store Intelligence addresses these challenges by converting raw customer and sales data into actionable business insights.

---

## 💡 Solution

Purplle Store Intelligence provides a unified dashboard for:

### Customer Journey Tracking

* Track customer movement across store zones
* Reconstruct customer paths
* Analyze engagement patterns
* Monitor zone transitions

### Footfall Analytics

* Track entries and exits
* Measure real-time occupancy
* Identify peak traffic periods
* Calculate conversion rates

### Revenue Intelligence

* Department-wise revenue analysis
* Revenue distribution across store zones
* Identification of high-performing categories
* Sales trend monitoring

### Conversion Funnel Analysis

* Track customer progression through the store
* Identify drop-off points
* Measure funnel performance
* Improve conversion efficiency

### Business Insights Engine

* Automated store recommendations
* Peak sales hour detection
* Top-performing zone identification
* Salesperson performance analysis

---

## 🏗️ System Architecture

```text
Video Cameras
        ↓
YOLOv8 Person Detection
        ↓
ByteTrack Tracking
        ↓
Zone Mapping Engine
        ↓
SQLite Database
        ↓
FastAPI Backend
        ↓
React Dashboard
        ↓
Store Intelligence Insights
```

---

## 🛠️ Tech Stack

### Frontend

* React.js
* Recharts
* Axios
* Framer Motion

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

## 📂 Project Structure

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

---

## 🔌 API Endpoints

### Metrics

```http
GET /api/v1/metrics
```

### Insights

```http
GET /api/v1/insights
```

### Conversion Funnel

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

## ⚙️ Local Setup

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

#### Windows

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

Backend will run at:

```text
http://127.0.0.1:8000
```

### Run Frontend

```bash
cd frontend

npm install

npm start
```

Frontend will run at:

```text
http://localhost:3000
```

---

## 📈 Business Impact

Purplle Store Intelligence enables:

* Better merchandising decisions
* Improved workforce allocation
* Enhanced customer journey visibility
* Increased store efficiency
* Higher conversion rates
* Data-driven retail operations

By transforming raw customer movement and sales data into actionable recommendations, the platform helps retail managers optimize store performance and improve business outcomes.

---

## 🎥 Submission Assets

### Live Application

https://purplle-store-intelligence-three.vercel.app

### Backend API

https://purplle-store-intelligence-dlca.onrender.com

### GitHub Repository

https://github.com/agrima29/purplle-store-intelligence

---

## 👩‍💻 Author

**Agrima Singh**

B.Tech Computer Science Engineering

Hackathon Submission – Purplle Tech Challenge 2026

Focused on customer journey analytics, footfall intelligence, conversion tracking, and revenue-driven retail insights.

---

## 🙏 Thank You

Purplle Store Intelligence demonstrates how computer vision and retail analytics can transform in-store activity into meaningful business intelligence, enabling smarter operational and merchandising decisions.
