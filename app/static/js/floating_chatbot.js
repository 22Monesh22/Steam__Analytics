class FloatingChatbot {
    constructor() {
        this.sessionId = null;
        this.isOpen = false;
        this.isMinimized = false;
        this.currentDashboard = '';
        this.init();
    }

    init() {
        this.createChatbotHTML();
        this.bindEvents();
        this.startSession();
        this.detectDashboard();
        
        console.log('🚀 Floating Chatbot initialized');
    }

    createChatbotHTML() {
        const chatbotHTML = `
        <div id="floating-chatbot" class="floating-chatbot">
            <!-- Chat Toggle Button -->
            <div id="chatToggle" class="chat-toggle">
                <div class="chat-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z" fill="currentColor"/>
                    </svg>
                </div>
                <div class="notification-dot"></div>
            </div>

            <!-- Chat Window -->
            <div id="chatWindow" class="chat-window">
                <div class="chat-header">
                    <div class="header-info">
                        <h3>Dashboard Assistant</h3>
                        <span class="status">Online</span>
                    </div>
                    <div class="header-actions">
                        <button id="minimizeBtn" class="header-btn" title="Minimize">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M18 15L12 9L6 15"/>
                            </svg>
                        </button>
                        <button id="closeBtn" class="header-btn" title="Close">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                </div>

                <div class="chat-messages" id="chatMessages">
                    <!-- Messages will appear here -->
                </div>

                <div class="suggestions-container" id="suggestionsContainer">
                    <div class="suggestions-header">
                        <span>💡 Quick Questions</span>
                    </div>
                    <div class="suggestions-grid" id="suggestionsGrid">
                        <!-- Suggestions will appear here -->
                    </div>
                </div>

                <div class="chat-input-container">
                    <div class="input-wrapper">
                        <textarea 
                            id="chatInput" 
                            placeholder="Ask about this dashboard..." 
                            rows="1"
                            maxlength="1000"
                        ></textarea>
                        <button id="sendBtn" class="send-button">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13"/>
                            </svg>
                        </button>
                    </div>
                    <div class="input-footer">
                        <span class="char-count">0/1000</span>
                        <span class="ai-badge">AI Powered</span>
                    </div>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        this.injectStyles();
    }

    injectStyles() {
        const styles = `
        <style>
            .floating-chatbot {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }

            .chat-toggle {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                border: 3px solid white;
                position: relative;
            }

            .chat-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
            }

            .notification-dot {
                position: absolute;
                top: -5px;
                right: -5px;
                width: 12px;
                height: 12px;
                background: #ef4444;
                border-radius: 50%;
                border: 2px solid white;
                display: none;
            }

            .chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 400px;
                height: 600px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
                display: none;
                flex-direction: column;
                border: 1px solid #e2e8f0;
                overflow: hidden;
            }

            .chat-window.active {
                display: flex;
            }

            .chat-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .header-info h3 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
            }

            .status {
                font-size: 12px;
                opacity: 0.9;
            }

            .header-actions {
                display: flex;
                gap: 8px;
            }

            .header-btn {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                color: white;
                cursor: pointer;
                padding: 6px;
                border-radius: 6px;
                transition: all 0.2s;
            }

            .header-btn:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8fafc;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }

            .message {
                display: flex;
                gap: 12px;
                animation: messageSlide 0.3s ease-out;
            }

            .message.user {
                flex-direction: row-reverse;
            }

            .message-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                flex-shrink: 0;
            }

            .message.user .message-avatar {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
            }

            .message.assistant .message-avatar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .message-content {
                max-width: 280px;
            }

            .message.user .message-content {
                margin-left: auto;
            }

            .message-bubble {
                padding: 12px 16px;
                border-radius: 16px;
                font-size: 14px;
                line-height: 1.4;
                word-wrap: break-word;
            }

            .message.user .message-bubble {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 6px;
            }

            .message.assistant .message-bubble {
                background: white;
                color: #1e293b;
                border: 1px solid #e2e8f0;
                border-bottom-left-radius: 6px;
            }

            .message-time {
                font-size: 11px;
                color: #94a3b8;
                margin-top: 4px;
            }

            .suggestions-container {
                padding: 16px 20px;
                border-top: 1px solid #e2e8f0;
                background: white;
            }

            .suggestions-header {
                font-size: 12px;
                font-weight: 600;
                color: #64748b;
                margin-bottom: 12px;
            }

            .suggestions-grid {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .suggestion-chip {
                padding: 8px 12px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 12px;
                color: #475569;
                cursor: pointer;
                transition: all 0.2s;
                text-align: left;
            }

            .suggestion-chip:hover {
                background: #667eea;
                color: white;
                transform: translateY(-1px);
            }

            .chat-input-container {
                padding: 16px 20px;
                border-top: 1px solid #e2e8f0;
                background: white;
            }

            .input-wrapper {
                display: flex;
                gap: 12px;
                align-items: flex-end;
            }

            #chatInput {
                flex: 1;
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                font-size: 14px;
                resize: none;
                outline: none;
                background: #f8fafc;
                font-family: inherit;
                line-height: 1.4;
                max-height: 120px;
                min-height: 44px;
            }

            #chatInput:focus {
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .send-button {
                width: 44px;
                height: 44px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 12px;
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
                flex-shrink: 0;
            }

            .send-button:hover:not(:disabled) {
                transform: scale(1.05);
            }

            .send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }

            .input-footer {
                display: flex;
                justify-content: space-between;
                margin-top: 8px;
                font-size: 11px;
                color: #94a3b8;
            }

            .typing-indicator {
                display: flex;
                gap: 12px;
                align-items: center;
            }

            .typing-dots {
                display: flex;
                gap: 4px;
                background: white;
                padding: 12px 16px;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }

            .typing-dots span {
                width: 6px;
                height: 6px;
                background: #94a3b8;
                border-radius: 50%;
                animation: typingBounce 1.4s ease-in-out infinite both;
            }

            .typing-dots span:nth-child(1) { animation-delay: 0s; }
            .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
            .typing-dots span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes typingBounce {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-3px); }
            }

            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
        `;

        if (!document.querySelector('style[data-floating-chatbot]')) {
            const styleElement = document.createElement('div');
            styleElement.innerHTML = styles;
            const styleTag = styleElement.querySelector('style');
            styleTag.setAttribute('data-floating-chatbot', 'true');
            document.head.appendChild(styleTag);
        }
    }

    bindEvents() {
        // Use event delegation for dynamically created elements
        document.addEventListener('click', (e) => {
            if (e.target.id === 'chatToggle' || e.target.closest('#chatToggle')) {
                this.toggleChat();
            }
            if (e.target.id === 'closeBtn' || e.target.closest('#closeBtn')) {
                this.closeChat();
            }
            if (e.target.id === 'minimizeBtn' || e.target.closest('#minimizeBtn')) {
                this.minimizeChat();
            }
            if (e.target.id === 'sendBtn' || e.target.closest('#sendBtn')) {
                this.sendMessage();
            }
            if (e.target.classList.contains('suggestion-chip')) {
                this.useSuggestion(e.target.textContent);
            }
        });

        // Enter key to send (Shift+Enter for new line)
        document.addEventListener('keydown', (e) => {
            if (e.target.id === 'chatInput' && e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        document.addEventListener('input', (e) => {
            if (e.target.id === 'chatInput') {
                this.resizeTextarea(e.target);
                this.updateCharCount(e.target.value.length);
            }
        });
    }

    async startSession() {
        try {
            const response = await fetch('/smart-chat/start-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();
            
            if (data.success) {
                this.sessionId = data.session_id;
                console.log('✅ Chat session started:', this.sessionId);
                this.loadWelcomeMessage();
            } else {
                console.error('❌ Failed to start session');
            }
        } catch (error) {
            console.error('❌ Session start error:', error);
            // Fallback: create local session ID
            this.sessionId = 'local_' + Date.now();
            this.loadWelcomeMessage();
        }
    }

    async loadWelcomeMessage() {
        const dashboardUrl = window.location.href;
        
        try {
            const response = await fetch(`/smart-chat/get-suggestions?dashboard_url=${encodeURIComponent(dashboardUrl)}`);
            const data = await response.json();
            
            let welcomeMessage = "👋 Hello! I'm your Dashboard Assistant. I can help you understand and analyze this dashboard.";

            if (data.success) {
                welcomeMessage += " What would you like to know about the data?";
                this.displaySuggestions(data.suggestions);
            }

            this.addMessage('assistant', welcomeMessage);
            
        } catch (error) {
            console.error('❌ Welcome message error:', error);
            this.addMessage('assistant', "👋 Hello! I'm your Dashboard Assistant. How can I help you understand this data today?");
            this.displaySuggestions([
                "What does this dashboard show?",
                "Explain the key metrics",
                "How to interpret the charts",
                "What insights can I get?"
            ]);
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        if (!input) return;
        
        const message = input.value.trim();

        if (!message || !this.sessionId) return;

        // Add user message
        this.addMessage('user', message);
        input.value = '';
        this.updateCharCount(0);
        this.resizeTextarea(input);

        // Hide suggestions
        this.hideSuggestions();

        // Show typing indicator
        this.showTyping();

        try {
            const response = await fetch('/smart-chat/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    dashboard_url: window.location.href,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();

            this.hideTyping();

            if (data.success) {
                this.addMessage('assistant', data.response);
                
                if (data.suggestions && data.suggestions.length > 0) {
                    this.displaySuggestions(data.suggestions);
                }
            } else {
                this.addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
            }

        } catch (error) {
            console.error('❌ Chat error:', error);
            this.hideTyping();
            this.addMessage('assistant', "I'm having trouble connecting right now. Please check your connection and try again.");
        }
    }

    addMessage(role, content) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const timestamp = new Date().toLocaleTimeString([], { 
            hour: '2-digit', minute: '2-digit' 
        });

        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${role === 'user' ? '👤' : '🤖'}
            </div>
            <div class="message-content">
                <div class="message-bubble">${this.formatMessage(content)}</div>
                <div class="message-time">${timestamp}</div>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Show notification if chat is closed
        if (role === 'assistant' && !this.isOpen) {
            this.showNotification();
        }
    }

    formatMessage(content) {
        if (!content) return '';
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
    }

    displaySuggestions(suggestions) {
        const container = document.getElementById('suggestionsGrid');
        if (!container) return;

        container.innerHTML = suggestions.map(suggestion => `
            <button class="suggestion-chip" title="${suggestion}">${suggestion}</button>
        `).join('');

        const suggestionsContainer = document.getElementById('suggestionsContainer');
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'block';
        }
    }

    hideSuggestions() {
        const container = document.getElementById('suggestionsContainer');
        if (container) {
            container.style.display = 'none';
        }
    }

    useSuggestion(suggestion) {
        const input = document.getElementById('chatInput');
        if (input) {
            input.value = suggestion;
            this.sendMessage();
        }
    }

    showTyping() {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typingIndicator';

        typingDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;

        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) {
            sendBtn.disabled = true;
        }
    }

    hideTyping() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) {
            sendBtn.disabled = false;
        }
    }

    showNotification() {
        const dot = document.querySelector('.notification-dot');
        if (dot) {
            dot.style.display = 'block';
        }
    }

    hideNotification() {
        const dot = document.querySelector('.notification-dot');
        if (dot) {
            dot.style.display = 'none';
        }
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chatWindow');
        
        if (this.isOpen && chatWindow) {
            chatWindow.classList.add('active');
            const input = document.getElementById('chatInput');
            if (input) input.focus();
            this.hideNotification();
        } else if (chatWindow) {
            chatWindow.classList.remove('active');
        }
    }

    closeChat() {
        this.isOpen = false;
        const chatWindow = document.getElementById('chatWindow');
        if (chatWindow) {
            chatWindow.classList.remove('active');
        }
    }

    minimizeChat() {
        this.isMinimized = !this.isMinimized;
        const chatWindow = document.getElementById('chatWindow');
        if (chatWindow) {
            chatWindow.style.display = this.isMinimized ? 'none' : 'flex';
        }
    }

    resizeTextarea(textarea) {
        if (!textarea) return;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    updateCharCount(count) {
        const counter = document.querySelector('.char-count');
        if (counter) {
            counter.textContent = `${count}/1000`;
        }
    }

    detectDashboard() {
        const url = window.location.href;
        this.currentDashboard = url;
        console.log('📊 Detected dashboard:', url);
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.floatingChatbot = new FloatingChatbot();
});