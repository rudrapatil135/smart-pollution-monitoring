let aqiData = [];
let sourceData = [];
let map;

/* =========================
   REVERSE GEOCODING (OSM)
========================= */
async function getLocationName(lat, lon) {
  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;

  try {
    const res = await fetch(url, {
      headers: { "Accept-Language": "en" }
    });
    const data = await res.json();

    return (
      data.address.suburb ||
      data.address.neighbourhood ||
      data.address.city ||
      data.address.town ||
      data.address.state ||
      "Unknown Location"
    );
  } catch {
    return "Unknown Location";
  }
}

/* =========================
   FETCH AQI DATA (WEEK 1)
========================= */
fetch("http://127.0.0.1:5000/aqi/realtime")
  .then(res => res.json())
  .then(payload => {
    aqiData = payload.data;
    renderAQI();
    initMap();
  });

/* =========================
   FETCH SOURCE DATA (WEEK 2)
========================= */
fetch("http://127.0.0.1:5000/aqi/source")
  .then(res => res.json())
  .then(payload => {
    sourceData = payload.points;
    renderCauses();
    addSourceMarkers();
  });

/* =========================
   AQI MONITORING SECTION
========================= */
async function renderAQI() {
  const table = document.getElementById("table");
  table.innerHTML = "";

  let sumAQI = 0;
  let maxAQI = 0;

  for (const p of aqiData) {
    const locationName = await getLocationName(p.latitude, p.longitude);

    sumAQI += p.aqi;
    maxAQI = Math.max(maxAQI, p.aqi);

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${locationName}</td>
      <td>${p.latitude.toFixed(2)}, ${p.longitude.toFixed(2)}</td>
      <td>${p.pm25}</td>
      <td>${p.aqi}</td>
      <td class="${p.category.toLowerCase()}">${p.category}</td>
    `;
    table.appendChild(row);
  }

  document.getElementById("avg").innerText =
    Math.round(sumAQI / aqiData.length);
  document.getElementById("max").innerText = maxAQI;
  document.getElementById("count").innerText = aqiData.length;
}

/* =========================
   CAUSE ANALYSIS (DONUTS)
========================= */
async function renderCauses() {
  const charts = document.getElementById("charts");
  charts.innerHTML = "";

  for (const p of sourceData) {
    const locationName = await getLocationName(p.latitude, p.longitude);

    const wrapper = document.createElement("div");
    wrapper.className = "donut-wrapper";

    wrapper.innerHTML = `
      <div class="donut-title">
        ${locationName}<br/>
      </div>
    `;

    const canvas = document.createElement("canvas");
    canvas.width = 180;
    canvas.height = 180;

    wrapper.appendChild(canvas);
    charts.appendChild(wrapper);

    new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: ["Traffic", "Regional Transport", "Background"],
        datasets: [{
          data: [
            p.sources.traffic,
            p.sources.regional_transport,
            p.sources.background
          ],
          backgroundColor: ["#dc2626", "#f59e0b", "#10b981"],
          borderWidth: 1
        }]
      },
      options: {
        responsive: false,
        cutout: "65%",
        plugins: {
          legend: { display: false },
          tooltip: { enabled: true }
        }
      }
    });
  }
}

/* =========================
   INITIALIZE MAP
========================= */
function initMap() {
  map = L.map("map").setView([28.6139, 77.2090], 10);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
  }).addTo(map);

  // AQI markers (Week 1)
  aqiData.forEach(async p => {
    const locationName = await getLocationName(p.latitude, p.longitude);

    L.circleMarker([p.latitude, p.longitude], {
      radius: 6,
      color: "#2563eb",
      fillOpacity: 0.8
    })
    .addTo(map)
    .bindPopup(`
      <b>${locationName}</b><br/>
      ${p.latitude}, ${p.longitude}<br/>
      AQI: ${p.aqi}
    `);
  });
}

/* =========================
   SOURCE MARKERS (WEEK 2)
========================= */
async function addSourceMarkers() {
  for (const p of sourceData) {
    const locationName = await getLocationName(p.latitude, p.longitude);
    const s = p.sources;

    let dominant = "background";
    let maxVal = s.background;

    if (s.traffic > maxVal) {
      dominant = "traffic";
      maxVal = s.traffic;
    }
    if (s.regional_transport > maxVal) {
      dominant = "regional_transport";
    }

    const colors = {
      traffic: "#dc2626",
      regional_transport: "#f59e0b",
      background: "#10b981"
    };

    L.circleMarker([p.latitude, p.longitude], {
      radius: 10,
      color: colors[dominant],
      fillOpacity: 0.9
    })
    .addTo(map)
    .bindPopup(`
      <b>${locationName}</b><br/>
      ${p.latitude}, ${p.longitude}<br/>
      <b>Dominant Source:</b> ${dominant}<br/>
      Traffic: ${s.traffic}%<br/>
      Regional: ${s.regional_transport}%<br/>
      Background: ${s.background}%
    `);
  }
}
