class ChatHistory {
    constructor() {
        this.storageKey = 'steam_chatbot_history';
        this.maxHistoryLength = 50; // Maximum conversations to store
        this.maxMessagesPerConversation = 100;
        this.currentConversationId = this.generateConversationId();
    }

    // Generate unique conversation ID
    generateConversationId() {
        return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Save message to history
    saveMessage(role, content, metadata = {}) {
        const message = {
            id: this.generateMessageId(),
            role: role,
            content: content,
            timestamp: new Date().toISOString(),
            conversationId: this.currentConversationId,
            ...metadata
        };

        const history = this.getHistory();
        let conversation = history.find(conv => conv.id === this.currentConversationId);

        if (!conversation) {
            conversation = {
                id: this.currentConversationId,
                title: this.generateConversationTitle(content),
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                messages: []
            };
            history.unshift(conversation);
        }

        conversation.messages.push(message);
        conversation.updatedAt = new Date().toISOString();

        // Trim messages if too long
        if (conversation.messages.length > this.maxMessagesPerConversation) {
            conversation.messages = conversation.messages.slice(-this.maxMessagesPerConversation);
        }

        // Trim history if too long
        if (history.length > this.maxHistoryLength) {
            history.splice(this.maxHistoryLength);
        }

        this.saveHistory(history);
        return message;
    }

    // Generate conversation title from first message
    generateConversationTitle(firstMessage) {
        const message = firstMessage.length > 50 ? firstMessage.substring(0, 47) + '...' : firstMessage;
        return `Chat: ${message}`;
    }

    // Get entire chat history
    getHistory() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error loading chat history:', error);
            return [];
        }
    }

    // Save history to localStorage
    saveHistory(history) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(history));
        } catch (error) {
            console.error('Error saving chat history:', error);
        }
    }

    // Get messages for current conversation
    getCurrentConversation() {
        const history = this.getHistory();
        return history.find(conv => conv.id === this.currentConversationId) || { messages: [] };
    }

    // Get all conversations (for history sidebar)
    getConversations() {
        return this.getHistory().map(conv => ({
            id: conv.id,
            title: conv.title,
            createdAt: conv.createdAt,
            updatedAt: conv.updatedAt,
            messageCount: conv.messages.length,
            preview: conv.messages.length > 0 ? this.getConversationPreview(conv.messages) : 'No messages'
        }));
    }

    // Get conversation preview text
    getConversationPreview(messages) {
        const lastMessage = messages[messages.length - 1];
        return lastMessage.content.length > 60 
            ? lastMessage.content.substring(0, 57) + '...' 
            : lastMessage.content;
    }

    // Load specific conversation
    loadConversation(conversationId) {
        this.currentConversationId = conversationId;
        const conversation = this.getCurrentConversation();
        return conversation.messages || [];
    }

    // Start new conversation
    startNewConversation() {
        this.currentConversationId = this.generateConversationId();
        return this.currentConversationId;
    }

    // Delete conversation
    deleteConversation(conversationId) {
        const history = this.getHistory();
        const filteredHistory = history.filter(conv => conv.id !== conversationId);
        this.saveHistory(filteredHistory);

        // If deleting current conversation, start new one
        if (conversationId === this.currentConversationId) {
            this.startNewConversation();
        }

        return filteredHistory;
    }

    // Clear all history
    clearAllHistory() {
        this.saveHistory([]);
        this.startNewConversation();
    }

    // Export history as JSON
    exportHistory() {
        const history = this.getHistory();
        const dataStr = JSON.stringify(history, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `steam-chatbot-history-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    // Import history from JSON
    importHistory(jsonData) {
        try {
            const importedHistory = JSON.parse(jsonData);
            
            if (Array.isArray(importedHistory)) {
                const currentHistory = this.getHistory();
                const mergedHistory = [...importedHistory, ...currentHistory]
                    .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
                    .slice(0, this.maxHistoryLength);
                
                this.saveHistory(mergedHistory);
                return { success: true, count: mergedHistory.length };
            } else {
                throw new Error('Invalid history format');
            }
        } catch (error) {
            console.error('Error importing history:', error);
            return { success: false, error: error.message };
        }
    }

    // Search through chat history
    searchHistory(query) {
        const history = this.getHistory();
        const results = [];

        history.forEach(conversation => {
            conversation.messages.forEach(message => {
                if (message.content.toLowerCase().includes(query.toLowerCase())) {
                    results.push({
                        conversationId: conversation.id,
                        conversationTitle: conversation.title,
                        message: message,
                        context: this.getMessageContext(conversation.messages, message.id)
                    });
                }
            });
        });

        return results;
    }

    // Get context around a message
    getMessageContext(messages, messageId, contextSize = 2) {
        const messageIndex = messages.findIndex(msg => msg.id === messageId);
        if (messageIndex === -1) return [];

        const start = Math.max(0, messageIndex - contextSize);
        const end = Math.min(messages.length, messageIndex + contextSize + 1);
        
        return messages.slice(start, end);
    }

    // Statistics
    getStatistics() {
        const history = this.getHistory();
        const totalMessages = history.reduce((sum, conv) => sum + conv.messages.length, 0);
        const totalConversations = history.length;
        
        const today = new Date();
        const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        
        const recentActivity = history.filter(conv => 
            new Date(conv.updatedAt) > lastWeek
        ).length;

        return {
            totalConversations,
            totalMessages,
            recentActivity,
            averageMessagesPerConversation: totalConversations > 0 ? (totalMessages / totalConversations).toFixed(1) : 0
        };
    }

    // Generate message ID
    generateMessageId() {
        return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Auto-cleanup old conversations
    autoCleanup(daysToKeep = 30) {
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);

        const history = this.getHistory();
        const filteredHistory = history.filter(conv => 
            new Date(conv.updatedAt) > cutoffDate
        );

        if (filteredHistory.length < history.length) {
            this.saveHistory(filteredHistory);
            return history.length - filteredHistory.length;
        }

        return 0;
    }
}

// Initialize and auto-cleanup on load
window.chatHistory = new ChatHistory();

// Auto-cleanup conversations older than 30 days
setTimeout(() => {
    const cleanedCount = window.chatHistory.autoCleanup(30);
    if (cleanedCount > 0) {
        console.log(`Auto-cleaned ${cleanedCount} old conversations`);
    }
}, 1000);