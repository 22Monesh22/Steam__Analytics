class ChatUI {
    constructor() {
        this.animationsEnabled = true;
    }

    // Smooth scroll to bottom of messages
    smoothScrollToBottom(container) {
        if (!this.animationsEnabled) {
            container.scrollTop = container.scrollHeight;
            return;
        }

        container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Add message with animation
    addMessageWithAnimation(messageElement, container) {
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(20px)';
        
        container.appendChild(messageElement);
        
        requestAnimationFrame(() => {
            messageElement.style.transition = 'all 0.3s ease';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        });
    }

    // Pulse animation for loading states
    createPulseAnimation(element) {
        element.style.animation = 'pulse 1.5s ease-in-out infinite';
    }

    // Remove pulse animation
    removePulseAnimation(element) {
        element.style.animation = 'none';
    }

    // Typing indicator animation
    startTypingAnimation(typingElement) {
        const dots = typingElement.querySelector('.typing-dots');
        if (dots) {
            dots.style.animation = 'typingBounce 1.4s ease-in-out infinite both';
        }
    }

    // Stop typing animation
    stopTypingAnimation(typingElement) {
        const dots = typingElement.querySelector('.typing-dots');
        if (dots) {
            dots.style.animation = 'none';
        }
    }

    // Shake animation for errors
    shakeElement(element) {
        element.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            element.style.animation = 'none';
        }, 500);
    }

    // Fade in suggestions
    fadeInSuggestions(suggestionsContainer) {
        suggestionsContainer.style.opacity = '0';
        suggestionsContainer.style.display = 'block';
        
        requestAnimationFrame(() => {
            suggestionsContainer.style.transition = 'opacity 0.3s ease';
            suggestionsContainer.style.opacity = '1';
        });
    }

    // Fade out suggestions
    fadeOutSuggestions(suggestionsContainer) {
        suggestionsContainer.style.transition = 'opacity 0.2s ease';
        suggestionsContainer.style.opacity = '0';
        
        setTimeout(() => {
            suggestionsContainer.style.display = 'none';
        }, 200);
    }

    // Highlight new message
    highlightMessage(messageElement) {
        messageElement.style.backgroundColor = 'rgba(102, 126, 234, 0.05)';
        messageElement.style.transition = 'background-color 0.3s ease';
        
        setTimeout(() => {
            messageElement.style.backgroundColor = '';
        }, 2000);
    }

    // Create loading skeleton for messages
    createMessageSkeleton(role) {
        const skeleton = document.createElement('div');
        skeleton.className = `message ${role}-message skeleton`;
        skeleton.innerHTML = `
            <div class="message-avatar">
                <div class="skeleton-avatar"></div>
            </div>
            <div class="message-content">
                <div class="skeleton-bubble">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line medium"></div>
                    <div class="skeleton-line long"></div>
                </div>
            </div>
        `;
        return skeleton;
    }

    // Remove skeleton
    removeSkeleton(skeletonElement) {
        skeletonElement.style.opacity = '0';
        setTimeout(() => {
            if (skeletonElement.parentNode) {
                skeletonElement.parentNode.removeChild(skeletonElement);
            }
        }, 300);
    }

    // Button press animation
    animateButtonPress(button) {
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 150);
    }

    // Notification animation for new messages
    notifyNewMessage() {
        const toggleBtn = document.getElementById('chatbotToggle');
        if (toggleBtn && !toggleBtn.classList.contains('active')) {
            this.createPulseAnimation(toggleBtn);
        }
    }

    // Stop notification animation
    stopNotification() {
        const toggleBtn = document.getElementById('chatbotToggle');
        if (toggleBtn) {
            this.removePulseAnimation(toggleBtn);
        }
    }
}

// CSS Animations (to be added to CSS file)
const chatAnimations = `
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.skeleton-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

.skeleton-bubble .skeleton-line {
    height: 12px;
    margin-bottom: 6px;
    border-radius: 6px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

.skeleton-line.short { width: 60%; }
.skeleton-line.medium { width: 80%; }
.skeleton-line.long { width: 95%; }

@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
`;

// Add animations to document
if (typeof document !== 'undefined') {
    const style = document.createElement('style');
    style.textContent = chatAnimations;
    document.head.appendChild(style);
}

window.chatUI = new ChatUI();