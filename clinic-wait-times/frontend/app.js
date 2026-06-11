document.getElementById('simulateCheckIn').addEventListener('click', async () => {
    // Simulate a new patient check‑in
    const patientId = 'p' + Math.floor(Math.random() * 1000).toString();
    const name = 'Patient ' + patientId;

    const payload = {
        patient_id: patientId,
        name: name,
        // Use the current time as check‑in time; converted to ISO string
        check_in_time: new Date().toISOString()
    };

    const resp = await fetch('/patients/check-in', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await resp.json();
    console.log('Check‑in response', data);
    // Force a refresh of the queue display to show latest state
    await refreshQueue();
});

async function refreshQueue() {
    // Refresh queue via REST and via WebSocket events
    const resp = await fetch('/queue');
    const queue = await resp.json();

    const rowsEl = document.getElementById('queueRows');
    rowsEl.innerHTML = '';
    for (const item of queue) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${item.name}</td><td>${new Date(item.check_in_time).toLocaleString()}</td><td>${Math.round(item.wait_time)}</td>`;
        if (item.longest_wait) {
            row.classList.add('longest-wait');
        }
        rowsEl.appendChild(row);
    }
    // Trigger a WebSocket ping to keep connection alive or fetch latest via SSE/WS as needed
    const ws = new WebSocket('ws://' + window.location.host + '/ws');
    // Send empty ping to keep alive; ignore response
    ws.send('');
}