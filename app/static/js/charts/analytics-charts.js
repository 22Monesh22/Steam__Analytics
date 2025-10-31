// Analytics chart initialization and management

class AnalyticsCharts {
    static init() {
        this.initializeGamesCharts();
        this.initializeUserCharts();
    }

    static initializeGamesCharts() {
        const popularGamesCtx = document.getElementById('popularGamesChart');
        if (popularGamesCtx) {
            this.createPopularGamesChart(popularGamesCtx);
        }

        const genreDistributionCtx = document.getElementById('genreDistributionChart');
        if (genreDistributionCtx) {
            this.createGenreDistributionChart(genreDistributionCtx);
        }
    }

    static initializeUserCharts() {
        const userGenresCtx = document.getElementById('userGenresChart');
        if (userGenresCtx) {
            this.createUserGenresChart(userGenresCtx);
        }

        const userTrendsCtx = document.getElementById('userTrendsChart');
        if (userTrendsCtx) {
            this.createUserTrendsChart(userTrendsCtx);
        }
    }

    static createPopularGamesChart(ctx) {
        // Sample data - in real app, this would come from API
        const data = {
            labels: ['Cyberpunk 2077', 'The Witcher 3', 'Baldur\'s Gate 3', 'Elden Ring', 'Red Dead Redemption 2'],
            datasets: [{
                label: 'Recommendations',
                data: [12500, 11800, 9800, 8700, 7600],
                backgroundColor: 'rgba(59, 130, 246, 0.8)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            }]
        };

        new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Recommendations: ${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Recommendations'
                        }
                    }
                }
            }
        });
    }

    static createGenreDistributionChart(ctx) {
        const data = {
            labels: ['Action', 'Adventure', 'RPG', 'Strategy', 'Simulation', 'Sports'],
            datasets: [{
                data: [25, 20, 18, 15, 12, 10],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
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
                    }
                }
            }
        });
    }

    static createUserGenresChart(ctx) {
        const data = {
            labels: ['Action', 'Adventure', 'RPG', 'Strategy', 'Indie'],
            datasets: [{
                label: 'User Preference %',
                data: [35, 25, 20, 12, 8],
                backgroundColor: 'rgba(139, 92, 246, 0.8)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 1
            }]
        };

        new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Preference %'
                        }
                    }
                }
            }
        });
    }

    static createUserTrendsChart(ctx) {
        const data = {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'New Users',
                    data: [1200, 1900, 1500, 2200, 1800, 2500],
                    borderColor: 'rgba(59, 130, 246, 1)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Active Users',
                    data: [8000, 8500, 9200, 8800, 9500, 9800],
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
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    AnalyticsCharts.init();
});