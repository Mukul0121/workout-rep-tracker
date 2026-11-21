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
    
    // Check if Nerd Mode is currently active so new rows inherit the state
    const isNerdMode = document.getElementById('nerd-toggle').checked;
    const hiddenClass = isNerdMode ? '' : 'hidden';

    sessions.forEach(s => {
        const date = s.created_at.split('T')[0];
        const mins = Math.floor(s.duration_sec / 60).toString().padStart(2, '0');
        const secs = (s.duration_sec % 60).toString().padStart(2, '0');
        const tut = s.tut_sec ? s.tut_sec.toFixed(1) + 's' : '0.0s';
        
        // Escape the JSON string so it safely passes into the HTML attribute
        const tempoData = (s.rep_tempos && s.rep_tempos !== '[]') ? s.rep_tempos.replace(/"/g, '&quot;') : null;
        
        let tempoBtn = '-';
        if (tempoData) {
            tempoBtn = `<button style="background: var(--glass-bg); border: 1px solid var(--accent); color: var(--accent); padding: 4px 10px; border-radius: 4px; cursor: pointer;" onclick="showTempo('${tempoData}', '${s.exercise}')">View</button>`;
        }
        
        tbody.innerHTML += `
            <tr>
                <td>${date}</td>
                <td style="text-transform: capitalize;">${s.exercise}</td>
                <td>${s.reps}</td>
                <td>${mins}:${secs}</td>
                <td class="nerd-col ${hiddenClass}">${tut}</td>
                <td class="nerd-col ${hiddenClass}">${tempoBtn}</td>
            </tr>
        `;
    });
    const dailyMap = {};
    sessions.forEach(s => {
        const date = s.created_at.split('T')[0];
        dailyMap[date] = (dailyMap[date] || 0) + s.reps;
    });

    const sortedDates = Object.keys(dailyMap).sort();
    const chartData = sortedDates.map(date => ({ day: date, reps: dailyMap[date] }));

    renderChart(chartData);
}

// Nerd Mode Toggle Logic
document.getElementById('nerd-toggle').addEventListener('change', function() {
    const label = document.getElementById('nerd-label');
    const nerdCols = document.querySelectorAll('.nerd-col');
    
    if (this.checked) {
        label.classList.add('active');
        nerdCols.forEach(col => col.classList.remove('hidden'));
    } else {
        label.classList.remove('active');
        nerdCols.forEach(col => col.classList.add('hidden'));
    }
});

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

// Globally accessible function to trigger the modal
window.showTempo = function(dataStr, exercise) {
    const data = JSON.parse(dataStr);
    const list = document.getElementById('tempo-list');
    list.innerHTML = '';
    
    // Accurately assign muscle contraction phases based on the lift mechanics
    const isCurl = exercise === 'curl';
    const flexLabel = isCurl ? 'Concentric (Up)' : 'Eccentric (Down)';
    const extendLabel = isCurl ? 'Eccentric (Down)' : 'Concentric (Up)';
    
    data.forEach(rep => {
        list.innerHTML += `
            <div style="border-bottom: 1px solid rgba(255,255,255,0.1); padding: 10px 0;">
                <div style="color: var(--text-muted); font-size: 0.8rem;">REP ${rep.rep}</div>
                <div><span style="color: #ef4444;">${flexLabel}:</span> ${rep.t_flex}s</div>
                <div><span style="color: var(--accent);">${extendLabel}:</span> ${rep.t_extend}s</div>
            </div>
        `;
    });
    
    document.getElementById('tempo-modal').showModal();
}

document.getElementById('exercise-filter').addEventListener('change', loadTable);
loadDashboard();