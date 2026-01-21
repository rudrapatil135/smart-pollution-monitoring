const map = L.map('map').setView([28.6139, 77.2090], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

const markerLayer = L.layerGroup().addTo(map);

function getAQIColorCategory(pm25) {
    if (pm25 <= 50) return { color: "#22c55e", category: "Good" };
    if (pm25 <= 100) return { color: "#facc15", category: "Moderate" };
    if (pm25 <= 150) return { color: "#fb923c", category: "Poor" };
    return { color: "#dc2626", category: "Severe" };
}

async function fetchAQI() {
    const res = await fetch("/api/aqi/");
    const result = await res.json();
    const data = result.data;

    markerLayer.clearLayers();

    // KPIs
    const pmValues = data.map(d => d.pm25);
    document.getElementById("avg").innerText =
        (pmValues.reduce((a, b) => a + b, 0) / pmValues.length).toFixed(2);

    document.getElementById("max").innerText = Math.max(...pmValues);
    document.getElementById("count").innerText = data.length;

    const tbody = document.getElementById("table");
    tbody.innerHTML = "";

    data.forEach(d => {
        const { color, category } = getAQIColorCategory(d.pm25);

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${d.station}</td>
            <td>${d.latitude.toFixed(4)}, ${d.longitude.toFixed(4)}</td>
            <td>${d.pm25}</td>
            <td>${d.pm25}</td>
            <td>${category}</td>
        `;
        tbody.appendChild(tr);

        L.circleMarker([d.latitude, d.longitude], {
            radius: 7,
            fillColor: color,
            color: "#000",
            weight: 1,
            fillOpacity: 0.8
        }).bindPopup(`
            <b>${d.station}</b><br>
            PM2.5: ${d.pm25}<br>
            Category: ${category}
        `).addTo(markerLayer);
    });
}

fetchAQI();
