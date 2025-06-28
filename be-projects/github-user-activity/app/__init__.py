from flask import Flask
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app 