from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
import json
import asyncio
from datetime import datetime
from collections import deque

app = FastAPI()

# In-memory data stores
patients = {}  # patient_id -> {name, reason, timestamp}
queue_order = deque()  # Ordered queue of patient keys
next_patient_id = 1

# Simulated backend queue processing
@app.get("/")
async def root():
    avg_wait = "0"
    longest_wait = "-"
    longest_name = "-"
    html = """
    <html>
    <head>
        <title>Clinic Wait-Time Board</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body { font-family: Arial; padding: 20px; background: #f2f2f2; }
            .board { background: white; padding: 20px; border-radius: 10px; }
            .patient { border-bottom: 1px solid #ccc; padding: 8px; display: flex; justify-content: space-between; }
            .longest { background-color: #ffdddd; font-weight: bold; }
            .form { margin-top: 20px; background: #f9f9f9; padding: 15px; border-radius: 8px; }
            input { padding: 5px; }
            button { padding: 5px 10px; }
        </style>
    </head>
    <body>
        <div class="board">
            <h1>Live Patient Queue</h1>
            <h2>Average Wait: <span id="avg-wait">{}</span> min</h2>
            <h2>Longest Wait: <span id="longest-wait">{}</span> min (Patient: <span id="longest-name">{}</span>)</h2>
            <div id="queue-list">
            </div>
            <div class="form">
                <h3>Check-In</h3>
                <form onsubmit="checkIn(event)">
                    <input type="text" id="patient-name" placeholder="Your name" required>
                    <input type="text" id="reason" placeholder="Reason (optional)">
                    <button type="submit">Check In</button>
                </form>
            </div>
        </div>
        <script>
        async function checkIn(event) {
            event.preventDefault();
            const name = document.getElementById('patient-name').value;
            const reason = document.getElementById('reason').value;
            await fetch('/api/check-in', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name, reason: reason})
            })
            .then(() => refreshQueue())
            .then(() => {
                document.getElementById('patient-name').value = '';
                document.getElementById('reason').value = '';
            });
        }
        async function refreshQueue() {
            const listEl = document.getElementById('queue-list');
            listEl.innerHTML = '';
            const res = await fetch('/api/queue');
            const data = await res.json();
            const queue = data['queue'];
            const avg = data['avg_wait'];
            const longest = data['longest'];
            document.getElementById('avg-wait').textContent = avg;
            document.getElementById('longest-wait').textContent = longest;
            document.getElementById('longest-name').textContent = longest !== '-' ? longest.patient_name : '-';
            queue.forEach(p => {
                const div = document.createElement('div');
                div.className = 'patient ' + (p.id == longest.id ? 'longest' : '');
                div.innerHTML = '<span>' + p.name + '</span><span>' + p.wait_minutes + ' min</span>';
                listEl.appendChild(div);
            });
        }
        setInterval(refreshQueue, 5000);
        window.onload = refreshQueue;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html.format(avg_wait, longest_wait, longest_name), status_code=200)
    
@app.get("/api/queue")
async def get_queue():
    if not queue_order:
        raise HTTPException(status_code=404, detail="No patients")
    now = datetime.now()
    wait_times = []
    for patient_key in queue_order:
        ts = patients[patient_key]['timestamp']
        patient_obj = patients[patient_key]
        wait = (now - ts).total_seconds() / 60
        wait_times.append(wait)
    avg_wait = int(sum(wait_times) / len(wait_times)) if wait_times else 0
    if wait_times:
        longest_idx = wait_times.index(max(wait_times))
        longest_patient_key = queue_order[longest_idx]
        longest_patient = patients[longest_patient_key]
        return {
            "queue": [{"id": p, "name": patients[p]['name'], "wait_minutes": int(wait_times[i]), "reason": patients[p].get('reason','')} 
                      for i, p in enumerate(queue_order)],
            "avg_wait": avg_wait,
            "longest": {"id": longest_patient_key, "patient_name": longest_patient['name'], "wait_minutes": int(max(wait_times))} 
        }
    return {"queue": [], "avg_wait": 0, "longest": "-"}
    
@app.post("/api/check-in")
async def check_in(data: dict):
    global next_patient_id
    patient_id = str(next_patient_id)
    next_patient_id += 1
    timestamp = datetime.now()
    patients[patient_id] = {
        "name": data["name"],
        "reason": data.get("reason", ""),
        "timestamp": timestamp,
    }
    queue_order.append(patient_id)
    return {"status": "ok", "patient_id": patient_id}
