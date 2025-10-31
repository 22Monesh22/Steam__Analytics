import uuid
from datetime import datetime, timedelta

class ConversationManager:
    """Manages chat memory and conversation flow"""
    
    def __init__(self):
        self.conversations = {}
        self.session_timeout = timedelta(hours=2)
    
    def create_session(self):
        """Create new conversation session"""
        session_id = str(uuid.uuid4())
        self.conversations[session_id] = {
            'messages': [],
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        return session_id
    
    def add_message(self, session_id, role, content, dashboard_context=None):
        """Add message to conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'messages': [],
                'created_at': datetime.now(),
                'last_activity': datetime.now()
            }
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now(),
            'dashboard_context': dashboard_context
        }
        
        self.conversations[session_id]['messages'].append(message)
        self.conversations[session_id]['last_activity'] = datetime.now()
        
        # Keep only last 20 messages to manage memory
        if len(self.conversations[session_id]['messages']) > 20:
            self.conversations[session_id]['messages'] = self.conversations[session_id]['messages'][-20:]
    
    def get_conversation_history(self, session_id, max_messages=10):
        """Get recent conversation history"""
        if session_id not in self.conversations:
            return []
        
        messages = self.conversations[session_id]['messages']
        return messages[-max_messages:] if messages else []
    
    def get_conversation_context(self, session_id):
        """Get formatted context for AI"""
        history = self.get_conversation_history(session_id)
        context = ""
        
        for msg in history:
            role = "User" if msg['role'] == 'user' else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        return context.strip()
    
    def generate_follow_ups(self, current_topic, dashboard_context):
        """Generate intelligent follow-up questions"""
        base_follow_ups = [
            "Would you like me to go deeper into this?",
            "Should I compare this with other metrics?",
            "Do you want to see the underlying data?",
            "Would a visual explanation help?"
        ]
        
        # Add context-specific follow-ups
        if 'sales' in current_topic.lower():
            base_follow_ups.extend([
                "Want to see sales by genre?",
                "Should I analyze seasonal trends?"
            ])
        elif 'user' in current_topic.lower():
            base_follow_ups.extend([
                "Want to see user demographics?",
                "Should I analyze engagement patterns?"
            ])
        
        return base_follow_ups[:4]
    
    def cleanup_old_sessions(self):
        """Remove expired sessions"""
        now = datetime.now()
        expired_sessions = []
        
        for session_id, data in self.conversations.items():
            if now - data['last_activity'] > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.conversations[session_id]