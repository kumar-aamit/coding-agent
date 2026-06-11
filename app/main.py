#!/usr/bin/env python
"""
Field Service Ticket Tracker Application
"""
import time
from datetime import datetime, timedelta
from app.models import Ticket

# Dummy data for demonstration
tickets = [
    {'id': 1, 'created_at': datetime.now() - timedelta(hours=2), 'priority': 'High', 'location': 'UC-BACK', 'status': 'Open', 'sla_deadline': datetime.now() + timedelta(minutes=30)},
    {'id': 2, 'created_at': datetime.now() - timedelta(hours=5), 'priority': 'Medium', 'location': 'UC-BACK', 'status': 'Open', 'sla_deadline': datetime.now() + timedelta(minutes=10)},
    {'id': 3, 'created_at': datetime.now() - timedelta(hours=1), 'priority': 'Low', 'location': 'UC-FRONT', 'status': 'Open', 'sla_deadline': datetime.now() + timedelta(minutes=45)},
]

def get_open_tickets():
    return [ticket for ticket in tickets if ticket['status'] == 'Open']

def oldest_open_ticket_age():
    open_tickets = get_open_tickets()
    if not open_tickets:
        return 0
    oldest = min(open_tickets, key=lambda x: x['created_at'])
    age = (datetime.now() - oldest['created_at']).total_seconds() / 60
    return age

def is_sla_breached(ticket):
    return ticket['sla_deadline'] < datetime.now()

def prioritize_and_assign_tickets():
    open_tickets = get_open_tickets()
    if not open_tickets:
        return None
    # Sort by priority (High > Medium > Low) and then by age
    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    sorted_tickets = sorted(open_tickets, key=lambda x: (priority_order[x['priority']], x['created_at']))
    # Assign the first ticket to a technician (simplified logic)
    assigned_ticket = sorted_tickets[0]
    return assigned_ticket

def simulate_ticket_stream():
    """Simulate incoming tickets every 2 minutes"""
    while True:
        # In a real app, this would fetch or generate new tickets
        time.sleep(120)
        new_ticket = {
            'id': len(tickets) + 1,
            'created_at': datetime.now(),
            'priority': 'High' if len(tickets) % 3 == 0 else 'Medium',
            'location': 'UC-BACK' if len(tickets) % 2 == 0 else 'UC-FRONT',
            'status': 'Open',
            'sla_deadline': datetime.now() + timedelta(minutes=30)
        }
        tickets.append(new_ticket)

if __name__ == '__main__':
    print(f"Oldest open ticket age: {oldest_open_ticket_age()} minutes")
    if open_tickets:
        oldest = oldest_open_ticket_age()
        if oldest > 30:  # SLA is 30 minutes
            print("SLA breach detected!")
    assigned_ticket = prioritize_and_assign_tickets()
    if assigned_ticket:
        print(f"Assigned ticket ID {assigned_ticket['id']} to nearest technician")

    # Start simulating tickets
    simulate_ticket_stream()