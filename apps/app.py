from pathlib import Path
from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

# SQLAlchemyなどインスタンス定義（関数の外）
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

def create_app():
    app = Flask(__name__)
    app.config.from_object(config["local"])
    app.config.from_mapping(
        SECRET_KEY='2AZSMss3p5QPbcY2hBsJ',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{str(Path(Path(__file__).parent.parent / "local.sqlite"))}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY='AuwzyszU5sugKN7KZs6f'
    )

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix='/auth')

    from apps.whisper import views as whisper_views
    app.register_blueprint(whisper_views.whisper_bp, url_prefix='/whisper')

    # ✅ 全ページログイン必須（except login/signup）
    @app.before_request
    def require_login():
        allowed_paths = ['/auth/login', '/auth/signup', '/static/', '/favicon.ico']
        if not current_user.is_authenticated:
            if all(not request.path.startswith(path) for path in allowed_paths):
                return redirect(url_for('auth.login', next=request.path))

    return app
