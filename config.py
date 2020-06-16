import os

basedir = os.path.abspath(os.path.dirname(__file__))

    
class Config:
    SECRET_KEY = 'guess'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False
    AAA = 'this is ProductionConfig'
    HOST = '0.0.0.0'
    PORT = 5001

    

class DevelopmentConfig(Config):
    DEBUG = True
    AAA = 'this is DevelopmentConfig'
    HOST = '127.0.0.1'
    PORT = 5001

    


class TestingConfig(Config):
    
    DEBUG = True
    AAA = 'this is TestingConfig'
    HOST = '0.0.0.0'
    PORT = 5001



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
