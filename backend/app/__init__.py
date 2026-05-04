from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Coolify/Heroku give 'postgres://' but modern SQLAlchemy requires 'postgresql://'
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    if not db_url:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        db_url = f"sqlite:///{os.path.join(base_dir, 'backend.db')}"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'fallback-secret')
    default_upload_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'uploads', 'menu_images')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', default_upload_folder)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    if db_url.startswith('sqlite'):
        with app.app_context():
            db.create_all()

    from flask import send_from_directory

    @app.route('/uploads/menu_images/<filename>')
    def serve_image(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    from app.routes.auth import auth_bp
    from app.routes.menu import menu_bp
    from app.routes.orders import orders_bp
    from app.routes.admin import admin_bp
    from app.routes.location import location_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(location_bp, url_prefix='/api/location')

    return app
