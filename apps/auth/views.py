from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user


# Blueprintでauthアプリを生成する
auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static'
)


# indexエンドポイントを作成し、index.htmlを返す
@auth.route('/')
def index():
    return render_template('auth/index.html')


@auth.route('/signup', methods=['GET','POST'])
def signup():
    # SignUpFormをインスタンス化する
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
        )
    
        # メールアドレス重複チェックをする
        if user.is_duplicate_email():
            flash('指定のメールアドレスは登録済みです')
            return redirect(url_for('auth.signup'))
        
        # ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()
        # ユーザー情報をセッションに格納する
        login_user(user)
        # GETパラメータにnextキーが存在し、値が無い場合はユーザーの一覧ページへリダイレクトする
        next_ = request.args.get('next')
        if next_ is None or not next_.startswith('/'):
            next_ = url_for('crud.users')
        return redirect(next_)

    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET','POST'])
def login():
    # LoginFormをインスタンス化する
    form = LoginForm()
    if form.validate_on_submit():
        # メールアドレスからユーザーを取得する
        user = User.query.filter_by(email=form.email.data).first()
    
        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('crud.users'))
        
        # ログイン失敗メッセージを設定する
        flash('メールアドレスかパスワードが不正です')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))