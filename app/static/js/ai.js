
class AIManager {
    constructor() {
        this.panel = document.getElementById('aiPanel');
        this.content = document.getElementById('aiContent');
    }

    async generateInsights(dataType) {
        try {
            this.showLoading();

            const response = await fetch('/api/generate-insights', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data_type: dataType,
                    timestamp: new Date().toISOString()
                })
            });

            const insights = await response.json();
            this.displayInsights(insights);
        } catch (error) {
            this.displayError('Failed to generate insights. Please try again.');
        }
    }

    showLoading() {
        this.content.innerHTML = `
            <div class="loading">
                <i class="fas fa-robot fa-spin"></i>
                <p>AI is analyzing your data...</p>
            </div>
        `;
        this.panel.style.display = 'block';
    }

    displayInsights(insights) {
        let html = '';

        if (insights.summary) {
            html += `<div class="insight-item">
                <h4><i class="fas fa-chart-line"></i> Summary</h4>
                <p>${insights.summary}</p>
            </div>`;
        }

        if (insights.key_findings && insights.key_findings.length > 0) {
            html += `<div class="insight-item">
                <h4><i class="fas fa-bullseye"></i> Key Findings</h4>
                <ul>${insights.key_findings.map(f => `<li>${f}</li>`).join('')}</ul>
            </div>`;
        }

        if (insights.recommendations && insights.recommendations.length > 0) {
            html += `<div class="insight-item">
                <h4><i class="fas fa-lightbulb"></i> Recommendations</h4>
                <ul>${insights.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>
            </div>`;
        }

        this.content.innerHTML = html;
    }

    displayError(message) {
        this.content.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>${message}</p>
            </div>
        `;
    }
}

// Global functions for HTML buttons
function generateAIInsights(dataType) {
    window.aiManager.generateInsights(dataType);
}

function closeAIPanel() {
    document.getElementById('aiPanel').style.display = 'none';
}

// Initialize AI Manager
document.addEventListener('DOMContentLoaded', () => {
    window.aiManager = new AIManager();
});