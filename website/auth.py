# website/auth.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # --- 优化点 1 ---
    # 如果用户已经通过后台验证为“已登录”状态，
    # 就直接将他重定向到主页，不再显示登录表单。
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    # --- 优化结束 ---

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Please check your email and password.', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # --- 优化点 2 ---
    # 同样的逻辑，如果用户已经登录，
    # 就没必要再注册新账号了，直接送回主页。
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    # --- 优化结束 ---

    if request.method == 'POST':
        email = request.form.get('email')
        # 在实际项目中，最好对 first_name 和 password 做一些基本的验证
        # 比如不能为空，密码长度等，这里为了简洁省略了
        first_name = request.form.get('first_name') 
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        else:
            new_user = User(
                email=email, 
                first_name=first_name, 
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            # 注册成功后自动登录，并跳转到主页
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("sign_up.html", user=current_user)
