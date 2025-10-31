// Dashboard functionality
class Dashboard {
    constructor() {
        this.init();
    }

    async init() {
        await this.loadData();
        this.updateStats();
        this.createCharts();
    }

    async loadData() {
        try {
            const [stats, clusters, popularity] = await Promise.all([
                this.fetchData('/api/stats'),
                this.fetchData('/api/user-clusters'),
                this.fetchData('/api/game-popularity')
            ]);

            this.data = {
                stats: stats.data,
                clusters: clusters.data,
                popularity: popularity.data
            };
        } catch (error) {
            console.error('Error loading data:', error);
        }
    }

    async fetchData(endpoint) {
        const response = await fetch(endpoint);
        return await response.json();
    }

    updateStats() {
        if (this.data.stats) {
            document.getElementById('totalUsers').textContent = this.data.stats.total_users.toLocaleString();
            document.getElementById('totalGames').textContent = this.data.stats.total_games.toLocaleString();
            document.getElementById('totalRecs').textContent = this.data.stats.total_recommendations.toLocaleString();
            document.getElementById('activeUsers').textContent = this.data.stats.active_users.toLocaleString();
        }
    }

    createCharts() {
        this.createUserClustersChart();
        this.createGamePopularityChart();
    }

    createUserClustersChart() {
        const ctx = document.getElementById('userClustersChart').getContext('2d');
        const clusterCounts = this.data.clusters.reduce((acc, user) => {
            acc[user.cluster] = (acc[user.cluster] || 0) + 1;
            return acc;
        }, {});

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(clusterCounts).map(k => `Cluster ${k}`),
                datasets: [{
                    data: Object.values(clusterCounts),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                }]
            }
        });
    }

    createGamePopularityChart() {
        const ctx = document.getElementById('gamePopularityChart').getContext('2d');
        const topGames = this.data.popularity.slice(0, 8);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: topGames.map(g => g.title.substring(0, 15) + '...'),
                datasets: [{
                    label: 'Popularity Score',
                    data: topGames.map(g => g.popularity_score),
                    backgroundColor: '#36A2EB'
                }]
            }
        });
    }
}

// AI Insights function
async function generateInsights(dataType) {
    try {
        const response = await fetch('/api/generate-insights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data_type: dataType })
        });

        const result = await response.json();
        displayInsights(result.insights);
    } catch (error) {
        displayInsights({ summary: 'Error generating insights: ' + error.message });
    }
}

function displayInsights(insights) {
    const content = `
        <h4>Summary</h4>
        <p>${insights.summary}</p>
        <h4>Key Findings</h4>
        <ul>${insights.key_findings.map(f => `<li>${f}</li>`).join('')}</ul>
        <h4>Recommendations</h4>
        <ul>${insights.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>
    `;
    document.getElementById('aiInsightsContent').innerHTML = content;
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});