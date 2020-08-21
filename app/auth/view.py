from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, logout_user, login_manager, login_required, current_user, login_user
from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@auth.route('/')
def index():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        existing_user = User.objects(username=form.username.data).first()
        if existing_user is None:
            username = form.username.data
            hashpass = generate_password_hash(form.password.data, method='sha256')
            user = User(username=username, password=hashpass)
            user.save()
            return redirect(url_for('auth.login'))
    return render_template('/auth/register.html', form=form)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(username=form.username.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('auth.dashboard'))
    return render_template('auth/login.html', form=form)

@auth.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return render_template('auth/login.html', form=LoginForm())
    users = []
    for u in User.objects(username=current_user.username):
        users.append({'username': u.username})
    return render_template('auth/dashboard.html', users=users, name=current_user.username)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
