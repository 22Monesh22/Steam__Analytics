// Chart initialization and management for dashboard

class DashboardCharts {
    static initPopularGamesChart() {
        const ctx = document.getElementById('popularGamesChart');
        if (!ctx) return;

        // Fetch data from API
        APIClient.get('/api/popular-games')
            .then(games => {
                const labels = games.map(game => game.name);
                const recommendations = games.map(game => game.recommendations);
                const ratings = games.map(game => game.rating);

                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Recommendations',
                                data: recommendations,
                                backgroundColor: 'rgba(59, 130, 246, 0.8)',
                                borderColor: 'rgba(59, 130, 246, 1)',
                                borderWidth: 1,
                                yAxisID: 'y'
                            },
                            {
                                label: 'Rating',
                                data: ratings,
                                type: 'line',
                                borderColor: 'rgba(16, 185, 129, 1)',
                                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                borderWidth: 2,
                                pointRadius: 4,
                                yAxisID: 'y1'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            mode: 'index',
                            intersect: false,
                        },
                        scales: {
                            x: {
                                ticks: {
                                    maxRotation: 45,
                                    minRotation: 45
                                }
                            },
                            y: {
                                type: 'linear',
                                display: true,
                                position: 'left',
                                title: {
                                    display: true,
                                    text: 'Recommendations'
                                }
                            },
                            y1: {
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: {
                                    display: true,
                                    text: 'Rating'
                                },
                                min: 0,
                                max: 5,
                                grid: {
                                    drawOnChartArea: false,
                                },
                            }
                        },
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        let label = context.dataset.label || '';
                                        if (label) {
                                            label += ': ';
                                        }
                                        if (context.dataset.label === 'Rating') {
                                            label += context.parsed.y.toFixed(2);
                                        } else {
                                            label += DashboardHelpers.formatNumber(context.parsed.y);
                                        }
                                        return label;
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error loading popular games chart:', error);
            });
    }

    static initGenreDistributionChart() {
        const ctx = document.getElementById('genreDistributionChart');
        if (!ctx) return;

        // Sample data - would come from API
        const data = {
            labels: ['Action', 'Adventure', 'Strategy', 'RPG', 'Simulation', 'Sports'],
            datasets: [{
                data: [1250, 890, 760, 680, 540, 320],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(236, 72, 153, 0.8)',
                    'rgba(6, 182, 212, 0.8)'
                ],
                borderWidth: 1
            }]
        };

        new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${DashboardHelpers.formatNumber(value)} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    static initTrendChart() {
        const ctx = document.getElementById('trendChart');
        if (!ctx) return;

        // Sample trend data
        const dates = [];
        for (let i = 30; i > 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            dates.push(date.toLocaleDateString());
        }

        const data = {
            labels: dates,
            datasets: [
                {
                    label: 'Daily Recommendations',
                    data: Array.from({length: 30}, () => Math.floor(Math.random() * 1000) + 500),
                    borderColor: 'rgba(59, 130, 246, 1)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'New Users',
                    data: Array.from({length: 30}, () => Math.floor(Math.random() * 100) + 50),
                    borderColor: 'rgba(16, 185, 129, 1)',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        };

        new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Count'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    DashboardCharts.initPopularGamesChart();
    
    // Initialize other charts if their elements exist
    if (document.getElementById('genreDistributionChart')) {
        DashboardCharts.initGenreDistributionChart();
    }
    
    if (document.getElementById('trendChart')) {
        DashboardCharts.initTrendChart();
    }
});

// Export for use in other modules
window.DashboardCharts = DashboardCharts;