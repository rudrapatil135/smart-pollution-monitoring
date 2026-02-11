fetch("{% url 'historical_trends_data' %}")

    .then(response => response.json())
    .then(data => {

        new Chart(document.getElementById("trendChart"), {
            type: "line",
            data: {
                labels: data.labels,
                datasets: data.datasets.map(ds => ({
                    ...ds,
                    tension: 0.4,
                    borderWidth: 2,
                    fill: false
                }))
            },
            options: {
                responsive: true,
                interaction: {
                    mode: "index",
                    intersect: false
                },
                plugins: {
                    legend: {
                        position: "top"
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Pollutant Level"
                        }
                    }
                }
            }
        });

    });
