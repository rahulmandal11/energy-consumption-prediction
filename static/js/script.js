// Tab functionality
function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove("active");
    }

    const tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Smooth scroll for hero button
function scrollToApp() {
    document.getElementById('app-section').scrollIntoView({ behavior: 'smooth' });
}

// Set today's date as default
window.onload = function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    document.getElementById('daily-date').value = today;
};

// Single prediction form logic
document.getElementById('single-prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const date = document.getElementById('date').value;
    const hour = document.getElementById('hour').value;

    const resultDiv = document.getElementById('single-result');
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('/predict_date', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: date,
                hour: parseInt(hour)
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('result-date').textContent = data.date;
            document.getElementById('result-hour').textContent = hour + ':00';
            document.getElementById('result-day').textContent = data.day_name;
            document.getElementById('result-consumption').textContent =
                data.prediction.toFixed(2) + ' ' + data.unit;

            resultDiv.style.display = 'block';
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

// Daily prediction form logic
let dailyChartInstance = null;

document.getElementById('daily-prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const date = document.getElementById('daily-date').value;

    const resultDiv = document.getElementById('daily-result');
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('/predict_day', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: date
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('total-daily').textContent =
                data.total_daily.toFixed(2) + ' ' + data.unit;
            document.getElementById('avg-hourly').textContent =
                data.average_hourly.toFixed(2) + ' ' + data.unit;

            // Create chart
            const ctx = document.getElementById('dailyChart').getContext('2d');

            if (dailyChartInstance) {
                dailyChartInstance.destroy();
            }

            const hours = data.hourly_predictions.map(p => p.hour + ':00');
            const consumptions = data.hourly_predictions.map(p => p.consumption);

            dailyChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: hours,
                    datasets: [{
                        label: 'Predicted Consumption (MWh)',
                        data: consumptions,
                        borderColor: '#2563eb', // Matches CSS var(--primary)
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Hourly Consumption Prediction - ' + data.date + ' (' + data.day_name + ')',
                            font: { size: 16, family: "'Inter', sans-serif" }
                        },
                        legend: {
                            display: true,
                            position: 'top',
                            labels: { font: { family: "'Inter', sans-serif" } }
                        }
                    },
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Consumption (MWh)',
                                font: { size: 14, family: "'Inter', sans-serif" }
                            },
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Hour of Day',
                                font: { size: 14, family: "'Inter', sans-serif" }
                            },
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        }
                    }
                }
            });

            resultDiv.style.display = 'block';
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

// Load statistics logic
async function loadStatistics() {
    const resultDiv = document.getElementById('stats-result');
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('/statistics');
        const data = await response.json();

        if (data.success) {
            const stats = data.statistics;

            document.getElementById('stat-mean').textContent = stats.mean.toFixed(2) + ' MWh';
            document.getElementById('stat-median').textContent = stats.median.toFixed(2) + ' MWh';
            document.getElementById('stat-std').textContent = stats.std.toFixed(2) + ' MWh';
            document.getElementById('stat-min').textContent = stats.min.toFixed(0) + ' MWh';
            document.getElementById('stat-max').textContent = stats.max.toFixed(0) + ' MWh';
            document.getElementById('stat-records').textContent = stats.total_records.toLocaleString();

            resultDiv.style.display = 'block';
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
}