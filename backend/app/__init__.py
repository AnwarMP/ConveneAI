from flask import Flask
from config import Config
from asgiref.wsgi import WsgiToAsgi
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],  # React's default port
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Wrap with ASGI for async support
    asgi_app = WsgiToAsgi(app)
    return asgi_app, app