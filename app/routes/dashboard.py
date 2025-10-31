from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import db
from app.models.game import Game
from app.models.insight import Insight
from app.services.bi_analyzer import BIAnalyzer
import json

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Main dashboard page"""
    return render_template('dashboard/index.html')

@dashboard_bp.route('/overview')
@login_required
def overview():
    """Dashboard overview with key metrics"""
    try:
        # Get analytics data
        bi_analyzer = BIAnalyzer()
        
        # Key metrics
        total_games = Game.query.count()
        total_insights = Insight.query.count()
        user_insights = Insight.query.filter_by(user_id=current_user.id).count()
        
        # Popular games
        popular_games = Game.query.order_by(Game.total_recommendations.desc()).limit(5).all()
        
        # Recent insights
        recent_insights = Insight.query.filter_by(user_id=current_user.id)\
            .order_by(Insight.created_at.desc()).limit(3).all()
        
        return render_template('dashboard/overview.html',
                            total_games=total_games,
                            total_insights=total_insights,
                            user_insights=user_insights,
                            popular_games=popular_games,
                            recent_insights=recent_insights)
    
    except Exception as e:
        flash('Error loading dashboard data.', 'error')
        return render_template('dashboard/overview.html')
    
@dashboard_bp.route('/documentation')
@login_required
def documentation():
    return render_template('documentation.html')

@dashboard_bp.route('/api/metrics')
@login_required
def get_metrics():
    """API endpoint for dashboard metrics"""
    try:
        bi_analyzer = BIAnalyzer()
        
        metrics = {
            'total_games': Game.query.count(),
            'total_users': current_user.query.count(),
            'total_recommendations': db.session.query(db.func.sum(Game.total_recommendations)).scalar() or 0,
            'avg_rating': db.session.query(db.func.avg(Game.rating)).scalar() or 0,
        }
        
        return jsonify(metrics)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/api/popular-games')
@login_required
def get_popular_games():
    """API endpoint for popular games data"""
    try:
        games = Game.query.order_by(Game.total_recommendations.desc()).limit(10).all()
        
        game_data = []
        for game in games:
            game_data.append({
                'name': game.name,
                'recommendations': game.total_recommendations,
                'rating': game.rating,
                'price': game.price
            })
        
        return jsonify(game_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500