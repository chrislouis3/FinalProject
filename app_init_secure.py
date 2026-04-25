# Improved app/__init__.py with Security Features
# ================================================

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os
import logging

db = SQLAlchemy()
csrf = CSRFProtect()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # ========== SECURITY CONFIGURATION ==========
    
    # Secret key for session management
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # CSRF Protection
    csrf.init_app(app)
    
    # Session security
    app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    
    # Database configuration
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'grades.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Prevent cache poisoning
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    
    db.init_app(app)
    
    # ========== SECURITY HEADERS MIDDLEWARE ==========
    @app.after_request
    def set_security_headers(response):
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # XSS Protection (legacy, but good for compatibility)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy (Feature Policy)
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
    
    # ========== ERROR HANDLING ==========
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {request.method} {request.path}")
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return {'error': 'Internal server error'}, 500
    
    # ========== REGISTER BLUEPRINTS ==========
    from app.routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # ========== CREATE DATABASE TABLES ==========
    with app.app_context():
        from app import models
        db.create_all()
        
        # Set restrictive permissions on database file
        import stat
        if os.path.exists(db_path):
            os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)  # 0600
            logger.info(f"Database created at {db_path} with secure permissions")
    
    logger.info(f"Application created in {config_name} mode")
    
    return app
