const API_URL = "http://127.0.0.1:5000/forecast?hours=48";

// Sidebar elements
const sidebar = document.getElementById("alertSidebar");
const closeBtn = document.getElementById("closeSidebar");

// Close sidebar
closeBtn.onclick = () => sidebar.classList.remove("active");

// Init map
const map = L.map("map").setView([28.6139, 77.2090], 10);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
}).addTo(map);

// Load data
fetch(API_URL)
    .then(res => res.json())
    .then(data => {
        data.forEach(loc => addMarker(loc));
    })
    .catch(err => console.error("API Error:", err));

function addMarker(location) {
    const current = location.forecast[0];
    const aqi = current.aqi;

    const style = getCircleStyle(aqi);

    const circle = L.circleMarker(
        [location.lat, location.lon],
        {
            radius: style.radius,
            fillColor: style.color,
            color: style.color,        // match border to fill
            weight: 1,
            opacity: 0.6,              // translucent border
            fillOpacity: 0.45          // translucent fill
        }
    ).addTo(map);

    circle.bindTooltip(
        `<b>${location.name}</b><br>AQI: ${Math.round(aqi)}`,
        { direction: "top", offset: [0, -6] }
    );

    circle.on("click", () => showAlertSidebar(location));
}

function getCircleStyle(aqi) {
    if (aqi <= 50) return {
        color: "#22c55e",
        radius: 7
    };

    if (aqi <= 100) return {
        color: "#facc15",
        radius: 9
    };

    if (aqi <= 200) return {
        color: "#fb923c",
        radius: 11
    };

    if (aqi <= 300) return {
        color: "#ef4444",
        radius: 13
    };

    return {
        color: "#7f1d1d",
        radius: 15
    };
}


function showAlertSidebar(location) {
    const current = location.forecast[0];

    document.getElementById("sidebarCity").innerText = location.name;
    document.getElementById("sidebarAQI").innerText =
        `AQI ${Math.round(current.aqi)}`;

    const level = getAQILevel(current.aqi);
    const levelBox = document.getElementById("sidebarLevel");

    levelBox.innerText = level.label;
    levelBox.style.background = level.color;

    // Advice
    const adviceList = document.getElementById("sidebarAdvice");
    adviceList.innerHTML = "";
    level.advice.forEach(text => {
        const li = document.createElement("li");
        li.innerText = text;
        adviceList.appendChild(li);
    });

    // Forecast summary
    document.getElementById("sidebarForecast").innerHTML = `
        <p><b>Next 24 hours:</b> Avg AQI ~ ${avgAQI(location.forecast.slice(0,24))}</p>
        <p><b>Next 48 hours:</b> Avg AQI ~ ${avgAQI(location.forecast.slice(0,48))}</p>
    `;

    sidebar.classList.add("active");
}

function avgAQI(list) {
    const sum = list.reduce((a, b) => a + b.aqi, 0);
    return Math.round(sum / list.length);
}

function getAQILevel(aqi) {
    if (aqi <= 50) return {
        label: "GOOD",
        color: "#22c55e",
        advice: [
            "Air quality is clean and healthy.",
            "Ideal for outdoor exercise and daily activities."
        ]
    };

    if (aqi <= 100) return {
        label: "MODERATE",
        color: "#facc15",
        advice: [
            "Air quality is acceptable.",
            "Sensitive individuals should avoid prolonged exertion."
        ]
    };

    if (aqi <= 200) return {
        label: "POOR",
        color: "#fb923c",
        advice: [
            "Breathing discomfort possible.",
            "Limit outdoor activity, especially for children and elderly."
        ]
    };

    if (aqi <= 300) return {
        label: "VERY POOR",
        color: "#ef4444",
        advice: [
            "High health risk for everyone.",
            "Avoid outdoor exposure.",
            "Use masks and air purifiers indoors."
        ]
    };

    return {
        label: "SEVERE",
        color: "#7f1d1d",
        advice: [
            "Serious health effects expected.",
            "Remain indoors with windows closed.",
            "Follow official health advisories strictly."
        ]
    };
}
