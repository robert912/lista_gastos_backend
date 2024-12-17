class Config(object):
    SECRET_KEY = 'f0faa2bed03b28e48544762d760aa169'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345678@host.docker.internal:3306/proyecto_devops" #Windows
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://robert:Trebor.912@172.17.0.1:3306/lista_gastos" #Ubuntu
    SQLALCHEMY_POOL_RECYCLE = 300
    DEBUG = True
    SQLALCHEMY_ECHO = True
    REDIS_URL = "redis://@redis:6379/0"

class TestingConfig(Config):
    """
    Testing configurations
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:12345678@curso-devops.cxuiediqujvr.us-west-2.rds.amazonaws.com:3306/proyecto_devops"
    SQLALCHEMY_POOL_RECYCLE = 300
    TESTING = True 
    DEBUG = True
    REDIS_URL = "redis://@redis:6379/0"

class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:toor@192.168.0.1:3306/database"
    SQLALCHEMY_POOL_RECYCLE = 300
    REDIS_URL = "redis://@redis:6379/0"

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
