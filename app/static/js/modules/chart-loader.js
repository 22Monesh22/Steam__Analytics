// Chart loading and management module

class ChartLoader {
    static charts = new Map();
    
    static init() {
        this.loadAllCharts();
        this.setupChartAutoRefresh();
    }
    
    static loadAllCharts() {
        // Initialize all charts on the page
        const chartElements = document.querySelectorAll('[data-chart]');
        
        chartElements.forEach(element => {
            const chartType = element.getAttribute('data-chart');
            const chartId = element.id;
            
            if (chartId) {
                this.loadChart(chartId, chartType, element);
            }
        });
    }
    
    static loadChart(chartId, chartType, element) {
        const ctx = element.getContext('2d');
        const config = this.getChartConfig(chartType, element);
        
        if (config) {
            const chart = new Chart(ctx, config);
            this.charts.set(chartId, chart);
        }
    }
    
    static getChartConfig(chartType, element) {
        const dataUrl = element.getAttribute('data-url');
        const config = {
            type: chartType,
            data: {},
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        };
        
        // Load data from URL if provided
        if (dataUrl) {
            this.loadChartData(dataUrl, element)
                .then(data => {
                    const chart = this.charts.get(element.id);
                    if (chart) {
                        chart.data = data;
                        chart.update();
                    }
                })
                .catch(error => {
                    console.error('Error loading chart data:', error);
                });
        }
        
        return config;
    }
    
    static async loadChartData(url, element) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching chart data:', error);
            
            // Return fallback data
            return this.getFallbackData(element);
        }
    }
    
    static getFallbackData(element) {
        const chartType = element.getAttribute('data-chart');
        
        switch (chartType) {
            case 'bar':
                return {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                    datasets: [{
                        label: 'Sample Data',
                        data: [65, 59, 80, 81, 56],
                        backgroundColor: 'rgba(59, 130, 246, 0.8)'
                    }]
                };
                
            case 'line':
                return {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Trend',
                        data: [30, 45, 35, 50],
                        borderColor: 'rgba(16, 185, 129, 1)',
                        tension: 0.4
                    }]
                };
                
            case 'doughnut':
                return {
                    labels: ['Category A', 'Category B', 'Category C'],
                    datasets: [{
                        data: [40, 35, 25],
                        backgroundColor: [
                            'rgba(59, 130, 246, 0.8)',
                            'rgba(16, 185, 129, 0.8)',
                            'rgba(139, 92, 246, 0.8)'
                        ]
                    }]
                };
                
            default:
                return { labels: [], datasets: [] };
        }
    }
    
    static setupChartAutoRefresh() {
        // Auto-refresh charts every 5 minutes
        setInterval(() => {
            this.refreshAllCharts();
        }, 5 * 60 * 1000);
    }
    
    static refreshAllCharts() {
        this.charts.forEach((chart, chartId) => {
            const element = document.getElementById(chartId);
            const dataUrl = element?.getAttribute('data-url');
            
            if (dataUrl) {
                this.loadChartData(dataUrl, element)
                    .then(data => {
                        chart.data = data;
                        chart.update('none');
                    });
            }
        });
    }
    
    static refreshChart(chartId) {
        const chart = this.charts.get(chartId);
        const element = document.getElementById(chartId);
        
        if (chart && element) {
            const dataUrl = element.getAttribute('data-url');
            
            if (dataUrl) {
                this.loadChartData(dataUrl, element)
                    .then(data => {
                        chart.data = data;
                        chart.update();
                    });
            }
        }
    }
    
    static destroyChart(chartId) {
        const chart = this.charts.get(chartId);
        if (chart) {
            chart.destroy();
            this.charts.delete(chartId);
        }
    }
    
    static exportChart(chartId, format = 'png') {
        const chart = this.charts.get(chartId);
        if (chart) {
            const link = document.createElement('a');
            link.download = `chart-${chartId}-${new Date().toISOString().split('T')[0]}.${format}`;
            link.href = chart.toBase64Image();
            link.click();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    ChartLoader.init();
});

// Export for global access
window.ChartLoader = ChartLoader;