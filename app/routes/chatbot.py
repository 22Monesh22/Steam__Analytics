from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.services.chatbot_engine import UnlimitedChatbotEngine
import logging
import traceback

logger = logging.getLogger(__name__)

# Define blueprint
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """Main chatbot endpoint with beyond-thinking"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        logger.info(f"Beyond-thinking chat request from user {current_user.id}: {user_message}")
        
        # Use UNLIMITED chatbot engine
        chatbot = UnlimitedChatbotEngine()
        result = chatbot.process_query(user_message, {
            'user_id': current_user.id,
            'username': current_user.username
        })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Unlimited chatbot route error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'response': 'I apologize for the technical issue. My thinking capabilities remain unlimited though! Feel free to ask me anything about Steam analytics, gaming industry, technology, or even creative ideas.',
            'is_beyond_application': True
        }), 500

@chatbot_bp.route('/welcome', methods=['GET'])
@login_required
def get_welcome_message():
    """Get welcome message and initial suggestions"""
    try:
        chatbot = UnlimitedChatbotEngine()
        welcome_data = chatbot.get_welcome_message()
        
        return jsonify(welcome_data)
        
    except Exception as e:
        logger.error(f"Welcome message error: {e}")
        return jsonify({
            'success': False,
            'response': "Hello! I'm your Steam Analytics Assistant. How can I help you today?",
            'suggested_questions': [
                "Show me sales trends",
                "Analyze user behavior",
                "What games are popular?"
            ]
        })

@chatbot_bp.route('/suggestions', methods=['GET'])
@login_required
def get_suggestions():
    """Get context-aware suggestions"""
    try:
        from app.services.dashboard_analyzer import DashboardAnalyzer
        analyzer = DashboardAnalyzer()
        
        # Get recent user queries or use default
        recent_context = request.args.get('context', '')
        dashboards = analyzer.identify_dashboard(recent_context)
        dashboard_ids = [dash['id'] for dash in dashboards]
        suggestions = analyzer.get_dashboard_suggestions(dashboard_ids)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'context': recent_context
        })
        
    except Exception as e:
        logger.error(f"Suggestions error: {e}")
        return jsonify({
            'success': False,
            'suggestions': [
                "Show me current trends",
                "Analyze user engagement",
                "What are popular genres?",
                "Give me platform overview"
            ]
        })

@chatbot_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'chatbot',
        'timestamp': '2024-01-01T00:00:00Z'
    })