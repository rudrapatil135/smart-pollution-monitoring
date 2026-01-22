// ================= MAP INITIALIZATION =================
let map = L.map('map').setView([28.6139, 77.2090], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let markers = [];

// ================= AQI CATEGORY BASED ON BACKEND AQI =================
function getAQIColorCategory(aqi) {
    if (aqi <= 50) return { color: '#00e400', category: 'Good' };
    if (aqi <= 100) return { color: '#ffff00', category: 'Moderate' };
    if (aqi <= 150) return { color: '#ff7e00', category: 'Unhealthy for Sensitive' };
    if (aqi <= 200) return { color: '#ff0000', category: 'Unhealthy' };
    if (aqi <= 300) return { color: '#8f3f97', category: 'Very Unhealthy' };
    return { color: '#7e0023', category: 'Hazardous' };
}

// ================= TABLE PAGINATION =================
let visibleCount = 5;
let viewMoreBtn;

// ================= FETCH AQI FROM BACKEND =================
async function fetchAQI() {
    try {
        const res = await fetch('/api/aqi/stations/');
        const result = await res.json();
        const data = result.data;

        // Clear previous markers
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        // ===== KPIs =====
        const aqiValues = data.map(d => d.aqi);
        document.getElementById('avg').innerText =
            (aqiValues.reduce((a, b) => a + b, 0) / aqiValues.length).toFixed(2);
        document.getElementById('max').innerText = Math.max(...aqiValues);
        document.getElementById('count').innerText = data.length;

        // ===== TABLE + MAP =====
        const tbody = document.getElementById('table');
        tbody.innerHTML = '';

        data.forEach(d => {
            const { color, category } = getAQIColorCategory(d.aqi);

            // Table row
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="place">${d.station}</td>
                <td>${d.latitude.toFixed(4)}, ${d.longitude.toFixed(4)}</td>
                <td>${d.pm25}</td>
                <td>${d.pm10}</td>
                <td>${d.aqi}</td>
                <td>
                    <span class="badge ${category.toLowerCase().replace(/ /g, '-')}">
                        ${category}
                    </span>
                </td>
            `;
            tbody.appendChild(tr);

            // Map marker
            const marker = L.circleMarker([d.latitude, d.longitude], {
                radius: 7,
                fillColor: color,
                color: '#000',
                weight: 1,
                fillOpacity: 0.75
            })
            .addTo(map)
            .bindPopup(`
                <b>${d.station}</b><br>
                PM2.5: ${d.pm25}<br>
                PM10: ${d.pm10}<br>
                AQI: ${d.aqi}<br>
                ${category}
            `);

            markers.push(marker);
        });

        // Update visible rows
        updateTable();

    } catch (err) {
        console.error("Station AQI fetch error:", err);
    }
}

// ================= UPDATE TABLE VISIBILITY =================
function updateTable() {
    const rows = document.querySelectorAll('#table tr');
    rows.forEach((row, index) => {
        row.style.display = index < visibleCount ? "" : "none";
    });

    if (viewMoreBtn) {
        viewMoreBtn.innerText = visibleCount >= rows.length ? "Show Less" : "View More";
    }
}

// ================= DOM READY =================
document.addEventListener("DOMContentLoaded", () => {
    viewMoreBtn = document.getElementById("viewMoreBtn");

    viewMoreBtn.addEventListener("click", () => {
        const rows = document.querySelectorAll('#table tr');
        visibleCount = visibleCount >= rows.length ? 5 : visibleCount + 15;
        updateTable();
    });

    fetchAQI();
    setInterval(fetchAQI, 300000); // refresh every 5 minutes
});
