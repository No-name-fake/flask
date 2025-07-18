from pathlib import Path


base_dir = Path(__file__).parent.parent


# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = '2AZSMss3p5QPbcY2hBsJ',
    WTF_CSRF_SECRET_KEY='AuwzyszU5sugKN7KZs6f'


# BaseConfigクラスを継承して、LocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{base_dir / "local.sqlite"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # SQLをログに出力する


# BaseConfigクラスを継承して、TestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{base_dir / "testing.sqlite"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # CSRF保護を無効にする



# config辞書にマッピングする
config = {
    'local': LocalConfig,
    'testing': TestingConfig
}