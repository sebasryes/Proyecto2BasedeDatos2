from flask import Flask
from flask_cors import CORS

from .db import db  # conexión MongoDB
from .pedido import pedido_bp
from .usuario import usuario_bp
from .restaurantes import restaurantes_bp
from .articulos_menu import menu_bp
from .resena import resena_bp

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS para todas las rutas
    CORS(app)

    # Registrar Blueprints
    app.register_blueprint(pedido_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(restaurantes_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(resena_bp)

    return app
