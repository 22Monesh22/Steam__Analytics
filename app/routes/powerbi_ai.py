from flask import Blueprint, request, jsonify, current_app
from app.services.powerbi_ai_service import PowerBILlmAgent
from app.services.real_data_analyzer import RealDataAnalyzer
import logging

logger = logging.getLogger(__name__)

# Initialize services
powerbi_ai_bp = Blueprint('powerbi_ai', __name__)
ai_agent = PowerBILlmAgent()
real_analyzer = RealDataAnalyzer()

@powerbi_ai_bp.route('/analyze-powerbi', methods=['POST'])
def analyze_powerbi():
    """Power BI AI analysis endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        dashboard_type = data.get('dashboard_type', 'game-analytics')
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        logger.info(f"Analyzing Power BI question: '{user_message}' for dashboard: {dashboard_type}")
        
        # Smart routing based on question type
        user_message_lower = user_message.lower()
        
        # Data questions - use real data analyzer
        data_keywords = ['how many', 'count', 'total', 'number of', 'records', 'data', 'csv', 'dataset']
        # Power BI questions - use AI agent
        powerbi_keywords = ['how to', 'use', 'navigate', 'filter', 'chart', 'graph', 'dashboard', 'explain']
        
        if any(keyword in user_message_lower for keyword in data_keywords):
            logger.info("Using Real Data Analyzer for data question")
            result = real_analyzer.analyze_question(user_message)
        elif any(keyword in user_message_lower for keyword in powerbi_keywords):
            logger.info("Using Power BI AI Agent for guidance question")
            result = ai_agent.process_query(user_message, dashboard_type, "web_user")
        else:
            logger.info("Using AI Agent for general question")
            result = ai_agent.process_query(user_message, dashboard_type, "web_user")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Power BI analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'response': f'I encountered an error: {str(e)}. Please try again.'
        }), 500

@powerbi_ai_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'operational',
        'services': {
            'powerbi_ai': 'ready',
            'real_data_analyzer': 'ready'
        }
    })