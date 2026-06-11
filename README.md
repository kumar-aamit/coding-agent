# Field Service Ticket Tracker

This application simulates a field service ticket tracking system for utilities and telecom. It includes:

1. Ticket management (creation, status tracking)
2. Technician dispatch based on location and urgency
3. SLA breach detection with visual indicators
4. Docker containerization for deployment

## Project Structure
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
```

## Application Overview
The app will simulate field service tickets with attributes like:
- ticket_id: Unique identifier
- created_at: Creation timestamp
- priority: High/Medium/Low urgency level
- location: Geographic coordinates or service area
- status: Open/In Progress/Resolved
- sla_deadline: Service Level Agreement deadline

Key Features:
- Oldest open ticket age calculation
- SLA breach detection with visual indicators (red flag)
- Simulated ticket stream generation
- Technician assignment based on proximity and priority
- Backlog summary generation

## Technology Stack
- Python 3.8+

## Getting Started
```bash
# Clone the repository
git clone https://github.com/yourusername/field-service-ticket-tracker.git
cd field-service-ticket-tracker

# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py
```

## Running Tests
```bash
python -m pytest tests/
```

## Docker Deployment
To build and run the Docker container:

```bash
docker build -t field-service-ticket-tracker .
docker run -p 8080:8080 field-service-ticket-tracker
```

## License
[MIT License](https://opensource.org/licenses/MIT)