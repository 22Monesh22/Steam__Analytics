from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.services.premium_chatbot import PremiumChatbot
import logging
import uuid

logger = logging.getLogger(__name__)

premium_chatbot_bp = Blueprint('premium_chatbot', __name__)

@premium_chatbot_bp.route('/chat', methods=['POST'])
@login_required
def premium_chat():
    """Premium chatbot endpoint with emotional intelligence"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        logger.info(f"Premium chat request from user {current_user.id}: {user_message}")
        
        # Use premium chatbot
        chatbot = PremiumChatbot()
        result = chatbot.process_message(user_message, {
            'user_id': current_user.id,
            'username': current_user.username,
            'is_premium': True,
            'user_tier': 'premium'
        }, session_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Premium chatbot route error: {e}")
        return jsonify({
            'success': False,
            'response': "🌟 I appreciate your message! I'm currently enhancing my emotional intelligence capabilities to provide you with an even more meaningful conversation experience. Let's continue with renewed connection! 💫",
            'is_premium': True,
            'emotional_intelligence': True,
            'session_id': data.get('session_id', str(uuid.uuid4())) if 'data' in locals() else str(uuid.uuid4())
        }), 500

@premium_chatbot_bp.route('/welcome', methods=['GET'])
@login_required
def get_premium_welcome():
    """Get premium welcome message"""
    try:
        chatbot = PremiumChatbot()
        welcome_data = chatbot.get_premium_welcome({
            'user_id': current_user.id,
            'username': current_user.username,
            'is_premium': True
        })
        
        return jsonify(welcome_data)
        
    except Exception as e:
        logger.error(f"Premium welcome message error: {e}")
        return jsonify({
            'success': True,
            'response': "🌟 Welcome to Premium Emotional AI! I'm your intelligent companion with emotional intelligence and multi-domain expertise. I'm here to understand you and provide valuable insights across any topic you'd like to explore!",
            'suggestions': [
                "Discuss gaming analytics and trends",
                "Explore emotional intelligence",
                "Talk about technology innovations",
                "Brainstorm creative ideas",
                "Share business insights",
                "Have a meaningful conversation"
            ],
            'is_premium': True,
            'emotional_intelligence': True,
            'session_id': str(uuid.uuid4()),
            'welcome_style': 'premium'
        })

@premium_chatbot_bp.route('/health', methods=['GET'])
def premium_health_check():
    """Premium health check endpoint"""
    from datetime import datetime
    return jsonify({
        'status': 'premium_healthy',
        'service': 'premium_chatbot',
        'emotional_intelligence': True,
        'premium_features': True,
        'timestamp': datetime.now().isoformat()
    })
