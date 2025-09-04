# website/__init__.py (完善后)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fwefwfw fwfwfwf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # --- 关键修改：移除数据库创建逻辑 ---
    # from .models import User, Note
    # with app.app_context():
    #     db.create_all()
    # ------------------------------------
    # 数据库的创建和更新，将通过 Flask-Migrate 在命令行中完成。

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # --- 关键修改：修正笔误 ---
    @login_manager.user_loader
    def load_user(id):
        # 确保在使用前导入模型
        from .models import User
        return User.query.get(int(id))
    # --------------------------

    return app
