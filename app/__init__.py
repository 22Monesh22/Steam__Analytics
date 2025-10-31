from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
import logging

import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    # Create Flask app with custom template and static folders
    app = Flask(__name__,
                template_folder=Config.TEMPLATES_FOLDER,
                static_folder=Config.STATIC_FOLDER)
    app.config.from_object(Config)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # FAVICON ROUTE - ADD THIS INSIDE create_app()
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = "strong"
    
    # User loader callback
    with app.app_context():
        from app.models.user import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.analytics import analytics_bp
    from app.routes.ai import ai_bp
    from app.routes.admin import admin_bp
    
    from app.routes.dashboard_enhancer import dashboard_enhancer_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_enhancer_bp, url_prefix='/dashboard-enhancer')

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Register Chatbot blueprint
    try:
        from app.routes.chatbot import chatbot_bp
        app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
        logger.info("✅ Chatbot routes registered")
    except ImportError as e:
        logger.warning("⚠️ Chatbot routes not available: %s", e)
    
    # Register Premium Chatbot blueprint
    try:
        from app.routes.premium_chatbot import premium_chatbot_bp
        app.register_blueprint(premium_chatbot_bp, url_prefix='/premium-chatbot')
        logger.info("✅ Premium Chatbot routes registered")
    except ImportError as e:
        logger.warning("⚠️ Premium Chatbot routes not available: %s", e)
    
    # 🔥 FIXED: Use DIFFERENT URL prefixes to avoid conflicts
    try:
        from app.routes.dashboard_chatbot import dashboard_chat_bp
        app.register_blueprint(dashboard_chat_bp, url_prefix='/dashboard-chat')
        logger.info("✅ Dashboard Chatbot routes registered")
    except ImportError as e:
        logger.warning("⚠️ Dashboard Chatbot routes not available: %s", e)
    
    # 🔥 FIXED: PowerBI AI gets the /smart-chat prefix
    try:
        from app.routes.powerbi_ai import powerbi_ai_bp
        app.register_blueprint(powerbi_ai_bp, url_prefix='/smart-chat')
        logger.info("✅ PowerBI AI routes registered")
    except ImportError as e:
        logger.warning("⚠️ PowerBI AI routes not available: %s", e)
    
    # Register PowerBI blueprint if it exists
    try:
        from app.routes.powerbi import powerbi_bp
        app.register_blueprint(powerbi_bp, url_prefix='/powerbi')
        logger.info("✅ PowerBI routes registered")
    except ImportError as e:
        logger.warning("⚠️ PowerBI routes not available: %s", e)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Create database tables - IMPORT ALL MODELS FIRST
    with app.app_context():
        try:
            # Import all models to ensure they're registered with SQLAlchemy
            from app.models.user import User
            from app.models.insight import Insight  # Add this import
            
            # Now create all tables
            db.create_all()
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error("❌ Database creation error: %s", e)
    
    return app

# Export db for modules to use
__all__ = ['db', 'bcrypt', 'login_manager', 'create_app']