# FloodGuard — Flood & Drainage Analysis System

ระบบเว็บสำหรับวิเคราะห์น้ำท่วมและระบบระบายน้ำ พัฒนาด้วย Flask + SQLite โดยแยก Engineering Service ออกจาก Flask Route เพื่อรองรับแนวคิด OOP / OOAD

## Features

- Home / Landing Page
- Dashboard
- Flood Risk Analysis
- Rational Method
- Manning Equation
- Risk Level: Low / Moderate / High / Critical
- Analysis History
- Project Management
- Project Detail
- Drainage Asset Management
- Reports + Filters
- Settings
- Documentation
- Responsive UI
- SQLite database
- JavaScript Preview Calculation
- Service Layer architecture

## Project Structure

```text
flood_drainage_system_v2/
├── app.py
├── requirements.txt
├── README.md
├── database/
│   └── db.py
├── models/
├── services/
│   ├── engineering_service.py
│   ├── project_service.py
│   └── report_service.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── analysis.html
│   ├── projects.html
│   ├── project_detail.html
│   ├── drainage.html
│   ├── reports.html
│   ├── settings.html
│   └── about.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Run on Windows

```cmd
cd flood_drainage_system_v2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Engineering Calculation

### Rational Method

```text
Q = 0.00278 C I A
```

I = mm/hr and A = hectares.

### Manning Equation

```text
Q = (1/n) A R^(2/3) S^(1/2)
```

### Risk

```text
Utilization = Runoff / Pipe Capacity × 100
```

Prototype thresholds:

- Low: < 50%
- Moderate: 50–74%
- High: 75–89%
- Critical: >= 90%

## Architecture

```text
Browser
   ↓
Flask Routes
   ↓
Service Layer
   ├── EngineeringService
   ├── ProjectService
   └── ReportService
   ↓
SQLite
```

## Important

ระบบนี้เป็น educational prototype สำหรับการเรียนและการนำเสนอ ไม่ใช่โปรแกรมออกแบบงานระบายน้ำจริง ควรตรวจสอบข้อมูลและมาตรฐานทางวิศวกรรมโดยผู้เชี่ยวชาญก่อนใช้งานจริง
