from apps.crud.forms import UserForm
from flask import Flask, Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.crud.models import User
from flask_login import login_required


# BlueprintでCRUDアプリを生成する
crud = Blueprint(
    'crud',
    __name__,
    template_folder='templates',
    static_folder='static'
)


# indexエンドポイントを作成し、index.htmlを返す
@crud.route('/')
# デコレーターを追加する
@login_required
def index():
    return render_template('crud/index.html')


@crud.route('/sql')
@login_required
def sql():
    db.session.query(User).all()
    return 'コンソールログを確認して下さい'


@crud.route('/user/new', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    ユーザー新規登録エンドポイント
    :return: ユーザー新規登録フォームを表示する
    """
    # UserFormをインスタンス化する
    form = UserForm()
    
    if form.validate_on_submit():
        # ユーザーを作成する
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # ユーザーを追加してコミットする
        db.session.add(user)
        db.session.commit()
        # ユーザーの一覧画面へリダイレクトする
        return redirect(url_for('crud.users'))
    return render_template('crud/create.html', form=form)


@crud.route('/users')
@login_required
def users():
    """
    ユーザー一覧エンドポイント
    :return: ユーザー一覧を表示する
    """
    # ユーザーを全件取得する
    users = User.query.all()
    return render_template('crud/index.html', users=users)


# methodsにGETとPOSTを指定する
@crud.route('/users/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """
    ユーザー編集エンドポイント
    :param user_id: ユーザーID
    :return: ユーザー編集フォームを表示する
    """
    # UserFormをインスタンス化する
    form = UserForm()
    
    # Userモデルを利用してユーザーを取得する
    user = User.query.filter_by(id=user_id).first()

    # formからサブミットされた場合はユーザーを更新しユーザーの一覧画面へリダイレクトする
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('crud.users'))
    
    #　GETの場合はHTMLを返す
    return render_template('crud/edit.html', form=form, user=user)


@crud.route('/users/<user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('crud.users'))