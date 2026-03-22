from flask import Flask, redirect, url_for, session, jsonify
from config import Config
from models import db
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Critical for HTTPS session cookies on HF Spaces
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'basic'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from auth import auth as auth_blueprint
from main import main as main_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# ── DEBUG ROUTE — visit /debug after login attempt ──
@app.route('/debug')
def debug():
    return jsonify({
        'session': dict(session),
        'is_authenticated': current_user.is_authenticated,
        'secret_key_set': bool(app.config.get('SECRET_KEY')),
        'secret_key_length': len(app.config.get('SECRET_KEY', '')),
        'cookie_secure': app.config.get('SESSION_COOKIE_SECURE'),
        'cookie_samesite': app.config.get('SESSION_COOKIE_SAMESITE'),
        'session_protection': login_manager.session_protection,
    })

# Create tables on startup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False)