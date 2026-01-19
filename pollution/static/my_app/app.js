// ================= MAP INITIALIZATION =================
let map = L.map('map').setView([28.6139, 77.2090], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let markers = [];

// ================= AQI CATEGORY =================
function getAQIColorCategory(pm25) {
    if (pm25 <= 50) return { color: '#00e400', category: 'Good' };
    if (pm25 <= 100) return { color: '#ffff00', category: 'Moderate' };
    if (pm25 <= 150) return { color: '#ff7e00', category: 'Unhealthy for Sensitive' };
    if (pm25 <= 200) return { color: '#ff0000', category: 'Unhealthy' };
    if (pm25 <= 300) return { color: '#8f3f97', category: 'Very Unhealthy' };
    return { color: '#7e0023', category: 'Hazardous' };
}

// ================= PAGINATION =================
let rows = [];
let visibleCount = 5;
let viewMoreBtn;

// ================= PLACE CACHE =================
const placeCache = {};

// ================= BACKGROUND GEOCODING =================
async function updatePlaceName(lat, lon, marker, row) {
    const key = `${lat.toFixed(4)},${lon.toFixed(4)}`;

    if (placeCache[key]) {
        row.querySelector(".place").innerText = placeCache[key];
        marker.setPopupContent(marker.getPopup().getContent().replace("Loading...", placeCache[key]));
        return;
    }

    try {
        const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`,
            { headers: { "Accept-Language": "en", "User-Agent": "AQI-Dashboard" } }
        );

        const data = await res.json();
        const place =
            data.address.suburb ||
            data.address.neighbourhood ||
            data.address.city ||
            data.address.town ||
            data.address.village ||
            "Unknown Location";

        placeCache[key] = place;

        row.querySelector(".place").innerText = place;
        marker.setPopupContent(marker.getPopup().getContent().replace("Loading...", place));

    } catch (err) {
        console.error("Geocoding error:", err);
    }
}

// ================= RANDOM POINTS =================
function generateRandomPoints(n, latMin, latMax, lonMin, lonMax, pm25Range) {
    const points = [];
    for (let i = 0; i < n; i++) {
        points.push({
            latitude: Math.random() * (latMax - latMin) + latMin,
            longitude: Math.random() * (lonMax - lonMin) + lonMin,
            pm25: Math.floor(
                Math.random() * (pm25Range.max - pm25Range.min) + pm25Range.min
            )
        });
    }
    return points;
}

// ================= UPDATE TABLE =================
function updateTable() {
    rows.forEach((row, index) => {
        row.style.display = index < visibleCount ? "" : "none";
    });

    viewMoreBtn.innerText =
        visibleCount >= rows.length ? "Show Less" : "View More";
}

// ================= FETCH AQI =================
async function fetchAQI() {
    try {
        const res = await fetch('/api/aqi/?city=Delhi');
        const result = await res.json();
        let data = result.data || [];

        // Clear map
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        // Generate demo points
        const minPM = Math.min(...data.map(d => d.pm25), 50);
        const maxPM = Math.max(...data.map(d => d.pm25), 200);

        const extraPoints = generateRandomPoints(
            Math.max(0, 150 - data.length),
            28.4, 28.9,
            76.9, 77.3,
            { min: minPM, max: maxPM }
        );

        data = data.concat(extraPoints);

        // ================= KPIs =================
        const pm25Values = data.map(d => d.pm25);
        document.getElementById('avg').innerText =
            (pm25Values.reduce((a, b) => a + b, 0) / pm25Values.length).toFixed(2);
        document.getElementById('max').innerText = Math.max(...pm25Values);
        document.getElementById('count').innerText = data.length;

        // ================= TABLE + MAP =================
        const tbody = document.getElementById('table');
        tbody.innerHTML = '';

        data.forEach(d => {
            const { color, category } = getAQIColorCategory(d.pm25);

            // ---- TABLE ROW (INSTANT) ----
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="place">Loading...</td>
                <td>${d.latitude.toFixed(4)}, ${d.longitude.toFixed(4)}</td>
                <td>${d.pm25}</td>
                <td>${d.pm25}</td>
                <td>
                    <span class="badge ${category.toLowerCase().replace(/ /g, '-')}">
                        ${category}
                    </span>
                </td>
            `;
            tbody.appendChild(tr);

            // ---- MAP MARKER ----
            const marker = L.circleMarker([d.latitude, d.longitude], {
                radius: 6,
                fillColor: color,
                color: '#000',
                weight: 1,
                fillOpacity: 0.7
            })
            .addTo(map)
            .bindPopup(`
                <b>Loading...</b><br>
                PM2.5: ${d.pm25}<br>
                ${category}
            `);

            markers.push(marker);

            // ---- BACKGROUND NAME UPDATE ----
            updatePlaceName(d.latitude, d.longitude, marker, tr);
        });

        // ================= PAGINATION INIT =================
        rows = document.querySelectorAll('#table tr');
        visibleCount = 5;
        updateTable();

    } catch (err) {
        console.error("AQI fetch error:", err);
    }
}

// ================= DOM READY =================
document.addEventListener("DOMContentLoaded", () => {
    viewMoreBtn = document.getElementById("viewMoreBtn");

    viewMoreBtn.addEventListener("click", () => {
        visibleCount = visibleCount >= rows.length ? 5 : visibleCount + 15;
        updateTable();
    });

    fetchAQI();
    setInterval(fetchAQI, 300000);
});
