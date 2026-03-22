from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import current_user
from models import User
from vision import describe_image

main = Blueprint('main', __name__)

def get_current_user():
    """Check flask-login first, fall back to manual session."""
    if current_user.is_authenticated:
        return current_user
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(int(user_id))
    return None

@main.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', user=user)

@main.route('/describe', methods=['POST'])
def describe():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    buddy_name = request.form.get('buddy', 'duck')

    if image_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        image_bytes = image_file.read()
        description = describe_image(image_bytes, buddy_name)
        return jsonify({'description': description})
    except Exception as e:
        return jsonify({'error': str(e)}), 500