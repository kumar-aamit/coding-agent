# Ticket model definition
class Ticket:
    def __init__(self, ticket_id, created_at, priority, location, status, sla_deadline):
        self.ticket_id = ticket_id
        self.created_at = created_at
        self.priority = priority
        self.location = location
        self.status = status
        self.sla_deadline = sla_deadline

    def is_sla_breached(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        return now > self.sla_deadline

    def time_since_creation(self):
        from datetime import datetime
        now = datetime.now()
        diff = now - self.created_at
        return diff.total_seconds() / 60  # Return minutes