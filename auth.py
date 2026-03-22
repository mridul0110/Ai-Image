from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth = Blueprint('auth', __name__)

# ── REGISTER ──────────────────────────────────────────
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name').strip()
        email    = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm  = request.form.get('confirm')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with that email already exists.', 'error')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        new_user  = User(name=name, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # Auto login after register
        login_user(new_user, remember=True)
        session['user_id'] = new_user.id
        session.permanent = True

        return redirect(url_for('main.dashboard'))

    return render_template('register.html')


# ── LOGIN ─────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email').strip().lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.password_hash:
            flash('No account found with that email.', 'error')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash('Wrong password. Try again.', 'error')
            return redirect(url_for('auth.login'))

        # Both flask-login AND manual session for reliability on HF Spaces
        login_user(user, remember=True)
        session['user_id'] = user.id
        session.permanent = True

        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


# ── LOGOUT ────────────────────────────────────────────
@auth.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))