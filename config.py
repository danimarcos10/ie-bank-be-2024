import os

class Config(object): 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    DEBUG = True

class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True

class DevelopmentConfig(Config):
    # Use DATABASE_URL if available (Azure deployment), otherwise build from individual vars
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=os.getenv('DBUSER'),
            dbpass=os.getenv('DBPASS'),
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )
    DEBUG = True