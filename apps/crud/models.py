from datetime import datetime

from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# db.Modelを継承したUserモデルを作成する
class User(db.Model, UserMixin):
    # テーブル名を指定する
    __tablename__ = 'users'
    # カラムを定義する
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email= db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # パスワードをセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError('読み取り不可')
    # パスワードをセットするためのセッター関数でハッシュ化されたパスワードをセットする
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # パスワードをチェックする
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # メールアドレス重複チェックをする
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None

# apps/whisper/models.py

class VoiceNote(db.Model):
    __tablename__ = "voice_notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    transcription = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)