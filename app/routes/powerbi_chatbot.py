from flask import Blueprint, request, jsonify, current_app
from services.powerbi_ai_service import PowerBIAIAgent

powerbi_chat_bp = Blueprint('powerbi_chat', __name__)
ai_agent = PowerBIAIAgent()

@powerbi_chat_bp.route('/powerbi-chat/analyze', methods=['POST'])
def analyze_powerbi():
    """Main endpoint for Power BI analysis"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        dashboard_type = data.get('dashboard_type', 'game-analytics')
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # Analyze question type
        question_analysis = ai_agent.detect_question_type(user_message)
        
        # Override with explicit dashboard type if provided
        if dashboard_type:
            question_analysis['dashboard'] = dashboard_type
        
        # Get appropriate dashboard URL and name
        dashboard_url, dashboard_name = ai_agent.get_dashboard_context(question_analysis['dashboard'])
        
        # Get AI analysis
        ai_response = ai_agent.analyze_dashboard_insights(
            user_question=user_message,
            dashboard_url=dashboard_url,
            dashboard_name=dashboard_name
        )
        
        # Get relevant suggestions
        suggestions = ai_agent.get_question_suggestions(question_analysis['type'])
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'question_type': question_analysis['type'],
            'dashboard_used': question_analysis['dashboard'],
            'suggestions': suggestions,
            'metrics_analyzed': question_analysis['metrics']
        })
        
    except Exception as e:
        current_app.logger.error(f"PowerBI chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'response': 'I apologize, but I encountered an error while analyzing the dashboard. Please try again.'
        }), 500

@powerbi_chat_bp.route('/powerbi-chat/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions for Power BI analysis"""
    try:
        dashboard_type = request.args.get('dashboard_type', 'game-analytics')
        
        suggestions_map = {
            'user-analytics': [
                "How many active players are there?",
                "What's the player retention rate?",
                "Show player demographic breakdown",
                "What are the engagement trends?",
                "How does playtime vary by region?",
                "What's the daily active users count?"
            ],
            'game-analytics': [
                "How many total games are in the catalog?",
                "What are the most popular game genres?",
                "Show revenue by game category",
                "How many new games were added recently?",
                "What are the top 10 games by player count?",
                "Show sales performance trends"
            ],
            'recommendation-engine': [
                "What games are recommended most often?",
                "How accurate are the recommendations?",
                "Show user preference patterns",
                "What similar games are suggested?",
                "How do recommendations vary by player type?",
                "What's the recommendation success rate?"
            ]
        }
        
        suggestions = suggestions_map.get(dashboard_type, [
            "How many total games are there?",
            "What are the key performance metrics?",
            "Show player engagement insights",
            "What are the revenue trends?"
        ])
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'dashboard_type': dashboard_type
        })
        
    except Exception as e:
        current_app.logger.error(f"Suggestions error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to load suggestions'
        }), 500

@powerbi_chat_bp.route('/powerbi-chat/dashboards', methods=['GET'])
def get_dashboards():
    """Get available dashboard information"""
    try:
        dashboards = {
            'user-analytics': {
                'name': 'User Analytics Dashboard',
                'description': 'Player demographics, engagement metrics, retention rates',
                'url': ai_agent.dashboards['dashboard_1']
            },
            'game-analytics': {
                'name': 'Game Analytics Dashboard', 
                'description': 'Game catalog, performance metrics, revenue analysis',
                'url': ai_agent.dashboards['dashboard_2']
            },
            'recommendation-engine': {
                'name': 'Recommendation Engine Dashboard',
                'description': 'Game suggestions, user preferences, similarity analysis',
                'url': ai_agent.dashboards['dashboard_3']
            }
        }
        
        return jsonify({
            'success': True,
            'dashboards': dashboards
        })
        
    except Exception as e:
        current_app.logger.error(f"Dashboards error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to load dashboard information'
        }), 500