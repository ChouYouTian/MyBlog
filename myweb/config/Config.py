import os


basedir = os.path.abspath(os.path.dirname(__file__))

def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY ="#230dec61-fee8-4ef2-a791-36f9e680c9fc"

class DevelopmentConfig(BaseConfig):

    # "SQLALCHEMY_DATABASE_URI"= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}:3306/{DBNAME}"

    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("test.db")



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}