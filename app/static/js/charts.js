
class ChartManager {
    constructor() {
        this.charts = {};
        this.init();
    }

    async init() {
        await this.loadData();
        this.createCharts();
    }

    async loadData() {
        try {
            const [clusters, popularity, trends] = await Promise.all([
                this.fetchData('/api/user-clusters'),
                this.fetchData('/api/game-popularity'),
                this.fetchData('/api/trends')
            ]);

            this.data = { clusters, popularity, trends };
            this.updateStats();
        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    async fetchData(endpoint) {
        const response = await fetch(endpoint);
        return await response.json();
    }

    updateStats() {
        document.getElementById('total-users').textContent =
            this.data.clusters.length.toLocaleString();
        document.getElementById('total-games').textContent =
            this.data.popularity.length.toLocaleString();
        document.getElementById('total-recommendations').textContent =
            (this.data.clusters.reduce((sum, user) => sum + user.game_id, 0)).toLocaleString();
    }

    createCharts() {
        this.createUserClustersChart();
        this.createGamePopularityChart();
    }

    createUserClustersChart() {
        const ctx = document.getElementById('userClustersChart').getContext('2d');

        const clusterData = this.data.clusters.reduce((acc, user) => {
            acc[user.cluster] = (acc[user.cluster] || 0) + 1;
            return acc;
        }, {});

        this.charts.userClusters = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(clusterData).map(k => `Cluster ${k}`),
                datasets: [{
                    data: Object.values(clusterData),
                    backgroundColor: [
                        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'
                    ],
                    borderWidth: 2,
                    borderColor: '#1a1a2e'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#ffffff' }
                    }
                }
            }
        });
    }

    createGamePopularityChart() {
        const ctx = document.getElementById('gamePopularityChart').getContext('2d');
        const topGames = this.data.popularity.slice(0, 10);

        this.charts.gamePopularity = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: topGames.map(game => game.title.substring(0, 20) + '...'),
                datasets: [{
                    label: 'Popularity Score',
                    data: topGames.map(game => game.popularity_score),
                    backgroundColor: '#E94560',
                    borderColor: '#E94560',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#ffffff' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#ffffff', maxRotation: 45 }
                    }
                }
            }
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chartManager = new ChartManager();
});