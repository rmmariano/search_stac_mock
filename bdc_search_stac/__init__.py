import os
from flask import Flask
from flask_cors import CORS

from bdc_search_stac.blueprint import blueprint
from bdc_search_stac.config import get_settings

def create_app(config):
    app = Flask(__name__)
    
    with app.app_context():
        app.config.from_object(config)
        app.register_blueprint(blueprint)

    return app

app = create_app(get_settings(os.environ.get('ENVIRONMENT', 'DevelopmentConfig')))

CORS(app, resorces={r'/d/*': {"origins": '*'}})