from flask import Flask
from config import Config
from asgiref.wsgi import WsgiToAsgi

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Wrap with ASGI for async support
    asgi_app = WsgiToAsgi(app)
    return asgi_app, app