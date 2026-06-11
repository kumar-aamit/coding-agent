---
name: "field-service-ticket-tracker"
description: "Code generation and version control init for Field Service Ticket Tracker app"
---

## Field Service Ticket Tracker App

This application simulates a field service ticket tracking system for utilities and telecom. It includes:

1. Ticket management (creation, status tracking)
2. Technician dispatch based on location and urgency
3. SLA breach detection with visual indicators
4. Docker containerization for deployment

### Project Structure
```
field-service-ticket-tracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── main.py
├── tests/
│   └── test_services.py
├── docker/
│   └── Dockerfile
├── requirements.txt
├── README.md
└── .dockerignore
