# 🏥 MedAsset Guardian

A full-stack medical equipment lifecycle management platform for tracking healthcare assets, monitoring operational health, and generating maintenance recommendations through automated risk assessment.

## Overview

MedAsset Guardian helps hospitals and healthcare facilities manage critical medical equipment throughout its lifecycle. The application provides centralized inventory management, usage tracking, inspection history, maintenance logging, and automated risk analysis to improve equipment reliability and support preventive maintenance.

The project was built to demonstrate modern full-stack software engineering practices using React, FastAPI, PostgreSQL, Docker, and SQLAlchemy.

---

## Features

### Equipment Inventory
- Register medical equipment
- View all equipment in a centralized dashboard
- Track operational status
- Configure maximum service-life thresholds

### Usage Tracking
- Log equipment usage
- Monitor cumulative operating cycles
- Calculate remaining service life

### Risk Assessment Engine
- Calculate equipment health scores
- Determine risk level (Low, Medium, High)
- Recommend maintenance actions
- Automatically update equipment status

### Maintenance & Inspection
- Record maintenance history
- Store inspection records
- Track equipment condition over time

### Dashboard
- Equipment inventory overview
- Operational status summary
- Equipment health information
- Risk assessment reports

---

## Tech Stack

### Frontend
- React
- JavaScript

### Backend
- FastAPI
- SQLAlchemy
- Alembic

### Database
- PostgreSQL

### DevOps
- Docker
- Docker Compose

---

## Architecture

```
React Frontend
       │
 REST API
       │
FastAPI Backend
       │
 SQLAlchemy ORM
       │
 PostgreSQL
```

---

## Database Schema

Current entities include:

- Assets
- Usage Logs
- Inspections
- Maintenance Logs

Relationships:

```
Asset
 ├── Usage Logs
 ├── Inspections
 └── Maintenance Logs
```

---

## Risk Assessment

The application evaluates equipment health based on lifecycle usage.

The risk engine calculates:

- Health Score (0–100)
- Remaining Service Life
- Equipment Status
- Risk Level
- Maintenance Recommendation

Example output:

```json
{
  "health_score": 92,
  "risk_level": "LOW",
  "recommended_status": "ACTIVE",
  "remaining_uses": 4200,
  "recommendation": "Continue normal operation."
}
```

---

## Running the Project

### Clone the repository

```bash
git clone https://github.com/gescobar19/summitsafe.git
cd summitsafe
```

### Start PostgreSQL

```bash
docker compose up -d
```

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

python -m uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd client

npm install

npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## API Endpoints

### Assets

```
GET    /assets
POST   /assets
```

### Usage

```
POST   /usage
```

### Risk Reports

```
GET    /risk-report/{asset_id}
```

### Maintenance

```
POST   /maintenance
GET    /maintenance/{asset_id}
```

---

## Example Equipment

- Ventilator
- Infusion Pump
- Defibrillator
- MRI Scanner
- CT Scanner
- Patient Monitor

---

## Future Improvements

- Authentication & user accounts
- Role-based access control
- Predictive maintenance using machine learning
- Maintenance scheduling
- Equipment calibration tracking
- Interactive dashboard charts
- Equipment search and filtering
- CSV/PDF reporting
- Notifications for maintenance due dates

---

## Learning Objectives

This project demonstrates experience with:

- Full-stack application development
- REST API design
- PostgreSQL database design
- SQLAlchemy ORM
- Alembic migrations
- Docker containerization
- React state management
- Risk analysis algorithms
- CRUD application architecture

---

## Author

**Genesis Escobar**

- Portfolio: https://gescobar19.github.io
- GitHub: https://github.com/gescobar19
- LinkedIn: https://linkedin.com/in/genesis-escobar-3381421b6
