let chartInstance = null;

async function loadDashboard() {
    const statsRes = await fetch('/api/stats');
    const stats = await statsRes.json();

    if (stats.sessions === 0) {
        document.getElementById('empty-state').classList.remove('hidden');
        document.getElementById('dashboard-content').classList.add('hidden');
        return;
    } else {
        document.getElementById('empty-state').classList.add('hidden');
        document.getElementById('dashboard-content').classList.remove('hidden');
    }

    document.getElementById('stat-sessions').innerText = stats.sessions;
    document.getElementById('stat-total').innerText = stats.total_reps;
    
    const bestSquat = stats.best.find(b => b.exercise === 'squat');
    document.getElementById('stat-best-squat').innerText = bestSquat ? bestSquat.best_reps : 0;
    
    const bestCurl = stats.best.find(b => b.exercise === 'curl');
    document.getElementById('stat-best-curl').innerText = bestCurl ? bestCurl.best_reps : 0;

    renderChart(stats.daily);
    loadTable();
}

async function loadTable() {
    const filter = document.getElementById('exercise-filter').value;
    const url = filter ? `/api/sessions?exercise=${filter}` : '/api/sessions';
    const res = await fetch(url);
    const sessions = await res.json();
    
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';
    
    sessions.forEach(s => {
        const date = s.created_at.split('T')[0];
        const mins = Math.floor(s.duration_sec / 60).toString().padStart(2, '0');
        const secs = (s.duration_sec % 60).toString().padStart(2, '0');
        
        tbody.innerHTML += `
            <tr>
                <td>${date}</td>
                <td style="text-transform: capitalize;">${s.exercise}</td>
                <td>${s.reps}</td>
                <td>${mins}:${secs}</td>
            </tr>
        `;
    });
}

function renderChart(dailyData) {
    const ctx = document.getElementById('repsChart').getContext('2d');
    const labels = dailyData.map(d => d.day);
    const data = dailyData.map(d => d.reps);

    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Reps',
                data: data,
                backgroundColor: '#22c55e',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

document.getElementById('exercise-filter').addEventListener('change', loadTable);
loadDashboard();