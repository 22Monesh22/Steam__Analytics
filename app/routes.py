from flask import Blueprint, render_template, jsonify, request

main_bp = Blueprint('main', __name__)

# Sample data
sample_data = {
    'stats': {
        'total_users': 12500,
        'total_games': 850, 
        'total_recommendations': 45600,
        'active_users': 3400
    },
    'user_clusters': [
        {'user_id': 1, 'cluster': 0, 'games_played': 12, 'recommendation_rate': 0.8},
        {'user_id': 2, 'cluster': 1, 'games_played': 38, 'recommendation_rate': 0.9},
        {'user_id': 3, 'cluster': 0, 'games_played': 9, 'recommendation_rate': 0.6}
    ],
    'game_popularity': [
        {'game_id': 1, 'title': 'The Witcher 3: Wild Hunt', 'popularity_score': 95},
        {'game_id': 2, 'title': 'Counter-Strike: Global Offensive', 'popularity_score': 92},
        {'game_id': 3, 'title': 'Dota 2', 'popularity_score': 89}
    ]
}

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/stats')
def api_stats():
    return jsonify({'success': True, 'data': sample_data['stats']})

@main_bp.route('/api/user-clusters')
def api_user_clusters():
    return jsonify({'success': True, 'data': sample_data['user_clusters']})

@main_bp.route('/api/game-popularity')
def api_game_popularity():
    return jsonify({'success': True, 'data': sample_data['game_popularity']})

@main_bp.route('/api/generate-insights', methods=['POST'])
def api_generate_insights():
    data = request.get_json()
    data_type = data.get('data_type', 'general')
    
    insights = {
        'summary': f'AI analysis of {data_type} shows strong user engagement patterns.',
        'key_findings': ['High retention rates', 'Growing user base'],
        'predictions': ['25% growth expected next quarter'],
        'recommendations': ['Continue current strategies']
    }
    
    return jsonify({'success': True, 'insights': insights})
    from flask import Blueprint, render_template, jsonify, request
from app.services.bi_analyzer import BIAnalyzer
from app.services.ai_insights import AIInsights

main_bp = Blueprint('main', __name__)
bi_analyzer = BIAnalyzer()
ai_insights = AIInsights()

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/stats')
def api_stats():
    """Real statistics from your CSV data"""
    stats = bi_analyzer.get_real_stats()
    return jsonify({'success': True, 'data': stats})

@main_bp.route('/api/user-clusters')
def api_user_clusters():
    """Real user clusters from your data"""
    clusters = bi_analyzer.analyze_real_user_clusters()
    return jsonify({'success': True, 'data': clusters})

@main_bp.route('/api/game-popularity')
def api_game_popularity():
    """Real game popularity from your data"""
    games = bi_analyzer.analyze_real_game_popularity()
    return jsonify({'success': True, 'data': games})

@main_bp.route('/api/generate-insights', methods=['POST'])
def api_generate_insights():
    """AI insights based on real data"""
    data = request.get_json()
    data_type = data.get('data_type', 'general')
    
    # Get real data for AI analysis
    if data_type == 'user_clusters':
        real_data = bi_analyzer.analyze_real_user_clusters()
    elif data_type == 'game_popularity':
        real_data = bi_analyzer.analyze_real_game_popularity()
    else:
        real_data = bi_analyzer.get_real_stats()
    
    insights = ai_insights.generate_insights(data_type, real_data)
    return jsonify({'success': True, 'insights': insights})