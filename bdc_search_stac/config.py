import os


def get_settings(env):
    return eval(env)


class Config():
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('KEYSYSTEM', 'bdc_search_stac')


class ProductionConfig(Config):
    DEVELOPMENT = False

class DevelopmentConfig(Config):
    # DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True


key = Config.SECRET_KEY

