from flask import Blueprint, render_template, jsonify, current_app
from flask_login import login_required
import os
import logging

powerbi_bp = Blueprint('powerbi', __name__)
logger = logging.getLogger(__name__)

# Demo Power BI URLs as fallback
DEMO_POWERBI_URLS = {
    'user_analytics': 'https://app.powerbi.com/view?r=eyJrIjoiZDVmOGZlZjMtZDA0MC00YzZkLWEzN2MtYjE2MjI4NmU3YmQ2IiwidCI6ImU0YTM0MjcxLWE4NDUtNDM0OS1iNGJkLWQxY2VhODJlODg5OCJ9',
    'game_analytics': 'https://app.powerbi.com/view?r=eyJrIjoiODk4OTg5ODk4OTg5ODk4OSIsInQiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAifQ',
    'recommendation_engine': 'https://app.powerbi.com/view?r=eyJrIjoiNzk4OTg5ODk4OTg5ODk4OSIsInQiOiIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAifQ'
}

def get_powerbi_urls():
    """Dynamically fetch Power BI URLs with fallback to demo URLs"""
    urls = {}
    for key, demo_url in DEMO_POWERBI_URLS.items():
        env_var_name = f'POWERBI_DASHBOARD_{list(DEMO_POWERBI_URLS.keys()).index(key) + 1}'
        env_url = os.getenv(env_var_name, '').strip()
        urls[key] = env_url if env_url else demo_url
    
    logger.info(f"PowerBI URLs loaded: {urls}")
    return urls

@powerbi_bp.route('/dashboards')
@login_required
def dashboards():
    """Power BI dashboards overview page"""
    dashboards = get_powerbi_urls()
    return render_template('dashboard/powerbi_dashboards.html', 
                         dashboards=dashboards)

@powerbi_bp.route('/user-analytics')
@login_required
def user_analytics():
    """User Analytics Power BI Dashboard"""
    urls = get_powerbi_urls()
    dashboard_url = urls['user_analytics']
    
    logger.info(f"User Analytics URL: {dashboard_url}")
    return render_template('dashboard/powerbi_embed.html',
                         dashboard_url=dashboard_url,
                         title="User Analytics Dashboard",
                         description="Comprehensive analysis of user behavior and engagement patterns")

@powerbi_bp.route('/game-analytics')
@login_required
def game_analytics():
    """Game Analytics Power BI Dashboard"""
    urls = get_powerbi_urls()
    dashboard_url = urls['game_analytics']
    
    logger.info(f"Game Analytics URL: {dashboard_url}")
    return render_template('dashboard/powerbi_embed.html',
                         dashboard_url=dashboard_url,
                         title="Game Analytics Dashboard",
                         description="Detailed insights into game performance and market trends")

@powerbi_bp.route('/recommendation-engine')
@login_required
def recommendation_engine():
    """Recommendation Engine Power BI Dashboard"""
    urls = get_powerbi_urls()
    dashboard_url = urls['recommendation_engine']
    
    logger.info(f"Recommendation Engine URL: {dashboard_url}")
    return render_template('dashboard/powerbi_embed.html',
                         dashboard_url=dashboard_url,
                         title="Recommendation Engine Dashboard",
                         description="AI-powered game recommendation insights and performance metrics")

@powerbi_bp.route('/api/dashboard-urls')
@login_required
def api_dashboard_urls():
    """API endpoint to get Power BI dashboard URLs"""
    return jsonify(get_powerbi_urls())

@powerbi_bp.route('/debug/env')
@login_required
def debug_env():
    """Debug endpoint to check environment variables"""
    env_info = {
        'POWERBI_DASHBOARD_1': os.getenv('POWERBI_DASHBOARD_1'),
        'POWERBI_DASHBOARD_2': os.getenv('POWERBI_DASHBOARD_2'),
        'POWERBI_DASHBOARD_3': os.getenv('POWERBI_DASHBOARD_3'),
        'using_demo_urls': not any([
            os.getenv('POWERBI_DASHBOARD_1'),
            os.getenv('POWERBI_DASHBOARD_2'), 
            os.getenv('POWERBI_DASHBOARD_3')
        ])
    }
    return jsonify(env_info)