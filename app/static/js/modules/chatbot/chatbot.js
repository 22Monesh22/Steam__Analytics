class SteamChatbot {
    constructor() {
        this.isOpen = false;
        this.unreadCount = 0;
        this.currentConversation = [];
        this.isLoading = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadWelcomeMessage();
    }

    initializeElements() {
        // Core elements
        this.toggleBtn = document.getElementById('chatbotToggle');
        this.chatWindow = document.getElementById('chatbotWindow');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendButton');
        this.unreadBadge = document.getElementById('unreadBadge');
        this.suggestionsGrid = document.getElementById('suggestionsGrid');
        
        // Action buttons
        this.minimizeBtn = document.getElementById('minimizeBtn');
        this.closeBtn = document.getElementById('closeBtn');
        this.charCount = document.getElementById('charCount');
    }

    bindEvents() {
        // Toggle chat window
        this.toggleBtn.addEventListener('click', () => this.toggleChat());
        this.toggleBtn.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') this.toggleChat();
        });

        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input character count
        this.chatInput.addEventListener('input', () => {
            this.charCount.textContent = this.chatInput.value.length;
        });

        // Window actions
        this.minimizeBtn.addEventListener('click', () => this.minimizeChat());
        this.closeBtn.addEventListener('click', () => this.closeChat());

        // Suggestion chips
        this.suggestionsGrid.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion-chip')) {
                this.useSuggestion(e.target.textContent);
            }
        });

        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.chatWindow.contains(e.target) && 
                !this.toggleBtn.contains(e.target) && 
                this.isOpen) {
                this.minimizeChat();
            }
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            this.chatWindow.classList.add('active');
            this.chatInput.focus();
            this.resetUnreadCount();
        } else {
            this.chatWindow.classList.remove('active');
        }
    }

    minimizeChat() {
        this.isOpen = false;
        this.chatWindow.classList.remove('active');
    }

    closeChat() {
        this.isOpen = false;
        this.chatWindow.classList.remove('active');
        this.showNotification('Chat closed. Click the chat button to reopen.');
    }

    async loadWelcomeMessage() {
        try {
            const response = await fetch('/chatbot/welcome');
            const data = await response.json();
            
            if (data.success) {
                this.displayWelcomeMessage(data);
            }
        } catch (error) {
            console.error('Failed to load welcome message:', error);
            this.displaySystemMessage('Welcome to Steam Analytics Assistant! How can I help you today?');
        }
    }

    displayWelcomeMessage(data) {
        this.messagesContainer.innerHTML = '';
        
        const welcomeTemplate = document.getElementById('welcomeMessageTemplate');
        const welcomeClone = welcomeTemplate.content.cloneNode(true);
        
        this.messagesContainer.appendChild(welcomeClone);
        this.displaySuggestions(data.suggested_questions);
    }

    displaySystemMessage(message) {
        const template = document.getElementById('systemMessageTemplate');
        const clone = template.content.cloneNode(true);
        
        clone.querySelector('.message-bubble').textContent = message;
        clone.querySelector('.message-time').textContent = this.getCurrentTime();
        
        this.messagesContainer.appendChild(clone);
        this.scrollToBottom();
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        
        if (!message || this.isLoading) return;
        
        // Add user message to UI
        this.addMessageToChat('user', message);
        this.chatInput.value = '';
        this.charCount.textContent = '0';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/chatbot/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                // Handle beyond-thinking responses differently
                if (data.is_beyond_application) {
                    this.handleBeyondThinkingResponse(data);
                } else {
                    this.addMessageToChat('assistant', data.response);
                }
                
                if (data.suggested_questions && data.suggested_questions.length > 0) {
                    this.displaySuggestions(data.suggested_questions);
                }
            } else {
                this.addMessageToChat('assistant', 
                    "I apologize, but I encountered an error. Please try again.");
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTypingIndicator();
            this.addMessageToChat('assistant', 
                "I'm having trouble connecting right now. Please check your internet connection and try again.");
        }
    }

    addMessageToChat(role, content) {
        const templateId = role === 'user' ? 'userMessageTemplate' : 'assistantMessageTemplate';
        const template = document.getElementById(templateId);
        const clone = template.content.cloneNode(true);
        
        clone.querySelector('.message-bubble').innerHTML = this.formatMessage(content);
        clone.querySelector('.message-time').textContent = this.getCurrentTime();
        
        this.messagesContainer.appendChild(clone);
        this.scrollToBottom();
        
        // Add to conversation history
        this.currentConversation.push({ role, content, timestamp: new Date() });
        
        // Update unread count if chat is minimized
        if (role === 'assistant' && !this.isOpen) {
            this.incrementUnreadCount();
        }
    }

    handleBeyondThinkingResponse(data) {
        // Add special styling for beyond-thinking responses
        const template = document.getElementById('assistantMessageTemplate');
        const clone = template.content.cloneNode(true);
        
        const messageBubble = clone.querySelector('.message-bubble');
        messageBubble.innerHTML = this.formatMessage(data.response);
        
        // Add beyond-thinking indicator
        if (data.is_beyond_application) {
            const thinkingTag = document.createElement('div');
            thinkingTag.className = 'beyond-thinking-tag';
            thinkingTag.innerHTML = '🚀 Expanded Thinking';
            messageBubble.parentNode.insertBefore(thinkingTag, messageBubble.nextSibling);
        }
        
        // Display domain context if available
        if (data.related_domains && data.related_domains.length > 0) {
            this.displayDomainContext(data.related_domains);
        }
        
        clone.querySelector('.message-time').textContent = this.getCurrentTime();
        this.messagesContainer.appendChild(clone);
        this.scrollToBottom();
    }

    displayDomainContext(domains) {
        const domainContext = document.createElement('div');
        domainContext.className = 'domain-context';
        domainContext.innerHTML = `
            <div class="domain-tags">
                ${domains.map(domain => 
                    `<span class="domain-tag">${this.formatDomainName(domain)}</span>`
                ).join('')}
            </div>
        `;
        
        this.messagesContainer.appendChild(domainContext);
        this.scrollToBottom();
    }

    formatDomainName(domain) {
        const domainMap = {
            'industry_analysis': '📈 Industry',
            'technical_innovation': '⚡ Innovation', 
            'user_experience': '👥 UX/Design',
            'business_growth': '💼 Business',
            'future_trends': '🔮 Future',
            'general_knowledge': '💡 Knowledge'
        };
        return domainMap[domain] || domain;
    }

    formatMessage(content) {
        // Basic formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    useSuggestion(suggestion) {
        this.chatInput.value = suggestion;
        this.charCount.textContent = suggestion.length;
        this.chatInput.focus();
    }

    displaySuggestions(suggestions) {
        if (!suggestions || suggestions.length === 0) return;
        
        this.suggestionsGrid.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const template = document.getElementById('suggestionChipTemplate');
            const clone = template.content.cloneNode(true);
            
            const chip = clone.querySelector('.suggestion-chip');
            chip.textContent = suggestion;
            
            this.suggestionsGrid.appendChild(clone);
        });
    }

    showTypingIndicator() {
        this.isLoading = true;
        this.sendBtn.disabled = true;
        
        const template = document.getElementById('typingIndicatorTemplate');
        const clone = template.content.cloneNode(true);
        
        this.messagesContainer.appendChild(clone);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isLoading = false;
        this.sendBtn.disabled = false;
        
        const indicators = this.messagesContainer.querySelectorAll('.typing-indicator');
        indicators.forEach(indicator => indicator.remove());
    }

    incrementUnreadCount() {
        this.unreadCount++;
        this.unreadBadge.textContent = this.unreadCount;
        this.unreadBadge.style.display = 'flex';
    }

    resetUnreadCount() {
        this.unreadCount = 0;
        this.unreadBadge.style.display = 'none';
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }

    showNotification(message) {
        // Simple notification implementation
        console.log('Notification:', message);
        // You can implement a toast notification system here
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.steamChatbot = new SteamChatbot();
});