let map;
let pollutantChart;

document.addEventListener('DOMContentLoaded', () => {
    initMap();
    fetchLatestData();
});

function initMap() {
    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO'
    }).addTo(map);
}

async function fetchLatestData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();

        if (data && data.length > 0) {
            const latest = data[0];
            updateDashboard(latest);
            renderMapMarkers(data);
            renderChart(latest);
        }
    } catch (err) {
        console.error('Error fetching dashboard data:', err);
    }
}

function updateDashboard(data) {
    const aqiVal = document.getElementById('aqiValue');
    const aqiCat = document.getElementById('aqiCategory');
    const locLabel = document.getElementById('locationLabel');

    aqiVal.innerText = data.aqi;
    aqiCat.innerText = data.category;
    locLabel.innerText = `${data.location} (${data.latitude}, ${data.longitude})`;

    // Color mapping
    const categoryColors = {
        'Good': '#10b981',
        'Moderate': '#f59e0b',
        'Unhealthy (Sensitive)': '#f97316',
        'Unhealthy': '#ef4444',
        'Very Unhealthy': '#a855f7',
        'Hazardous': '#881337'
    };

    aqiVal.style.color = categoryColors[data.category] || 'white';

    // Update individual stats
    document.getElementById('val-pm25').innerText = data.pm25 + ' µg/m³';
    document.getElementById('val-pm10').innerText = data.pm10 + ' µg/m³';
    document.getElementById('val-no2').innerText = data.no2 + ' µg/m³';
    document.getElementById('val-co').innerText = data.co + ' µg/m³';
    document.getElementById('val-o3').innerText = data.o3 + ' µg/m³';
    document.getElementById('val-so2').innerText = data.so2 + ' µg/m³';
}

function renderMapMarkers(records) {
    records.forEach(rec => {
        const color = getAqiColor(rec.category);
        const marker = L.circleMarker([rec.latitude, rec.longitude], {
            radius: 10,
            fillColor: color,
            color: "#fff",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);

        marker.bindPopup(`<b>${rec.location}</b><br>AQI: ${rec.aqi}<br>${rec.category}`);
    });

    // Center map on latest
    if (records.length > 0) {
        map.setView([records[0].latitude, records[0].longitude], 5);
    }
}

function getAqiColor(category) {
    const colors = {
        'Good': '#10b981',
        'Moderate': '#f59e0b',
        'Unhealthy (Sensitive)': '#f97316',
        'Unhealthy': '#ef4444',
        'Very Unhealthy': '#a855f7',
        'Hazardous': '#881337'
    };
    return colors[category] || '#ccc';
}

function renderChart(data) {
    const ctx = document.getElementById('pollutantChart').getContext('2d');

    if (pollutantChart) pollutantChart.destroy();

    pollutantChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['PM2.5', 'PM10', 'NO₂', 'CO', 'O₃', 'SO₂'],
            datasets: [{
                label: 'Concentration (µg/m³)',
                data: [data.pm25, data.pm10, data.no2, data.co / 100, data.o3, data.so2], // Scaling CO down for visibility
                backgroundColor: [
                    'rgba(56, 189, 248, 0.6)',
                    'rgba(129, 140, 248, 0.6)',
                    'rgba(168, 85, 247, 0.6)',
                    'rgba(244, 114, 182, 0.6)',
                    'rgba(251, 146, 60, 0.6)',
                    'rgba(45, 212, 191, 0.6)'
                ],
                borderColor: '#ffffff',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { ticks: { color: '#94a3b8' } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
