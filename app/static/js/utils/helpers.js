// Utility functions for the Steam Analytics Platform

class DashboardHelpers {
    static formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    static formatCurrency(amount) {
        return '$' + parseFloat(amount).toFixed(2);
    }

    static formatPercentage(value) {
        return (value * 100).toFixed(1) + '%';
    }

    static showLoading(element) {
        element.innerHTML = '<div class="flex items-center justify-center"><div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div></div>';
    }

    static showError(element, message) {
        element.innerHTML = `<div class="text-red-600 text-sm">${message}</div>`;
    }
}

// API Client
class APIClient {
    static async get(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    }

    static async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    }
}

// Dashboard Metrics Loader
class DashboardMetrics {
    static async loadMetrics() {
        try {
            const metrics = await APIClient.get('/api/metrics');
            
            // Update metric elements
            if (metrics.total_games !== undefined) {
                document.getElementById('total-games').textContent = DashboardHelpers.formatNumber(metrics.total_games);
            }
            if (metrics.total_users !== undefined) {
                document.getElementById('total-users').textContent = DashboardHelpers.formatNumber(metrics.total_users);
            }
            if (metrics.total_recommendations !== undefined) {
                document.getElementById('total-recommendations').textContent = DashboardHelpers.formatNumber(metrics.total_recommendations);
            }
            if (metrics.avg_rating !== undefined) {
                document.getElementById('avg-rating').textContent = metrics.avg_rating.toFixed(2);
            }
            
        } catch (error) {
            console.error('Error loading metrics:', error);
            // Set fallback values
            document.getElementById('total-games').textContent = 'N/A';
            document.getElementById('total-users').textContent = 'N/A';
            document.getElementById('total-recommendations').textContent = 'N/A';
            document.getElementById('avg-rating').textContent = 'N/A';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load metrics if on dashboard
    if (document.getElementById('total-games')) {
        DashboardMetrics.loadMetrics();
    }
    
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute z-50 px-2 py-1 text-xs text-white bg-gray-900 rounded shadow-lg';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + (rect.width - tooltip.offsetWidth) / 2) + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
});

// Export for use in other modules
window.DashboardHelpers = DashboardHelpers;
window.APIClient = APIClient;
window.DashboardMetrics = DashboardMetrics;