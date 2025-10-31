class ChatAPI {
    constructor() {
        this.baseURL = '';
        this.timeout = 30000; // 30 seconds
        this.retryAttempts = 3;
        this.retryDelay = 1000;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            timeout: this.timeout,
            ...options
        };

        // Add CSRF token if available
        const csrfToken = this.getCSRFToken();
        if (csrfToken) {
            config.headers['X-CSRF-Token'] = csrfToken;
        }

        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                const response = await fetch(url, config);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                return data;

            } catch (error) {
                console.warn(`API attempt ${attempt} failed:`, error);
                
                if (attempt === this.retryAttempts) {
                    throw new Error(`API request failed after ${this.retryAttempts} attempts: ${error.message}`);
                }
                
                // Wait before retrying
                await this.delay(this.retryDelay * attempt);
            }
        }
    }

    async sendMessage(message, context = {}) {
        try {
            const data = await this.request('/chatbot/chat', {
                method: 'POST',
                body: JSON.stringify({
                    message: message,
                    context: context,
                    timestamp: new Date().toISOString(),
                    platform: 'web'
                })
            });

            return {
                success: true,
                data: data,
                error: null
            };

        } catch (error) {
            console.error('Send message error:', error);
            return {
                success: false,
                data: null,
                error: this.formatErrorMessage(error)
            };
        }
    }

    async getWelcomeMessage() {
        try {
            const data = await this.request('/chatbot/welcome');
            return {
                success: true,
                data: data,
                error: null
            };
        } catch (error) {
            console.error('Welcome message error:', error);
            return {
                success: false,
                data: null,
                error: error.message
            };
        }
    }

    async getSuggestions(context = '') {
        try {
            const data = await this.request(`/chatbot/suggestions?context=${encodeURIComponent(context)}`);
            return {
                success: true,
                data: data,
                error: null
            };
        } catch (error) {
            console.error('Suggestions error:', error);
            return {
                success: false,
                data: null,
                error: error.message
            };
        }
    }

    async healthCheck() {
        try {
            const data = await this.request('/chatbot/health');
            return {
                success: true,
                data: data,
                error: null
            };
        } catch (error) {
            console.error('Health check error:', error);
            return {
                success: false,
                data: null,
                error: error.message
            };
        }
    }

    // Analytics tracking
    trackEvent(eventName, properties = {}) {
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                event_category: 'chatbot',
                ...properties
            });
        }

        // Custom analytics
        const analyticsData = {
            event: eventName,
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent,
            ...properties
        };

        this.logAnalytics(analyticsData);
    }

    logAnalytics(data) {
        // Send to your analytics endpoint
        fetch('/api/analytics/chatbot-events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        }).catch(error => {
            console.warn('Analytics logging failed:', error);
        });
    }

    // Utility methods
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }

    formatErrorMessage(error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            return 'Network error. Please check your internet connection.';
        }
        
        if (error.message.includes('timeout')) {
            return 'Request timeout. Please try again.';
        }

        if (error.message.includes('500')) {
            return 'Server error. Please try again later.';
        }

        return error.message || 'An unexpected error occurred.';
    }

    // Rate limiting helper
    createRateLimiter(limit, interval) {
        const calls = [];
        
        return function() {
            const now = Date.now();
            calls.push(now);
            
            // Remove calls outside the interval
            while (calls.length > 0 && calls[0] <= now - interval) {
                calls.shift();
            }
            
            return calls.length <= limit;
        };
    }

    // Message validation
    validateMessage(message) {
        if (!message || typeof message !== 'string') {
            return { valid: false, error: 'Message must be a non-empty string' };
        }

        if (message.trim().length === 0) {
            return { valid: false, error: 'Message cannot be empty' };
        }

        if (message.length > 500) {
            return { valid: false, error: 'Message too long (max 500 characters)' };
        }

        // Check for potentially harmful content
        const harmfulPatterns = [
            /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
            /javascript:/gi,
            /on\w+\s*=/gi
        ];

        for (const pattern of harmfulPatterns) {
            if (pattern.test(message)) {
                return { valid: false, error: 'Message contains invalid content' };
            }
        }

        return { valid: true, error: null };
    }

    // Session management
    getSessionId() {
        let sessionId = sessionStorage.getItem('chatbot_session_id');
        if (!sessionId) {
            sessionId = this.generateSessionId();
            sessionStorage.setItem('chatbot_session_id', sessionId);
        }
        return sessionId;
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Performance monitoring
    async measurePerformance(operation, fn) {
        const startTime = performance.now();
        
        try {
            const result = await fn();
            const duration = performance.now() - startTime;
            
            this.trackEvent('performance_metric', {
                operation: operation,
                duration: Math.round(duration),
                success: true
            });
            
            return result;
        } catch (error) {
            const duration = performance.now() - startTime;
            
            this.trackEvent('performance_metric', {
                operation: operation,
                duration: Math.round(duration),
                success: false,
                error: error.message
            });
            
            throw error;
        }
    }
}

// Export for use in other modules
window.chatAPI = new ChatAPI();