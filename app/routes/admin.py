from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from auth.middleware import role_required
from app.models.user import User
from app.models.game import Game
from app.models.insight import Insight
from app.models import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    """User management page"""
    try:
        users = User.query.order_by(User.created_at.desc()).limit(50).all()
        return render_template('admin/users.html', users=users)
    except Exception as e:
        return render_template('admin/users.html', error=str(e))

@admin_bp.route('/system')
@login_required
@role_required('admin')
def system():
    """System monitoring page"""
    try:
        # System statistics
        stats = {
            'total_users': User.query.count(),
            'total_games': Game.query.count(),
            'total_insights': Insight.query.count(),
            'active_sessions': 0,  # Would come from session tracking
            'system_health': 'healthy'
        }
        return render_template('admin/system.html', stats=stats)
    except Exception as e:
        return render_template('admin/system.html', error=str(e))

@admin_bp.route('/settings')
@login_required
@role_required('admin')
def settings():
    """Platform settings page"""
    return render_template('admin/settings.html')

@admin_bp.route('/api/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@role_required('admin')
def api_user_management(user_id):
    """API for user management"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'GET':
        return jsonify(user.to_dict())
    
    elif request.method == 'PUT':
        data = request.get_json()
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})