from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from courses.models import db
from courses.routes import courses_bp

def create_app():
    """Application factory: initializes Flask with SQLAlchemy ORM and Flask-Migrate."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    Migrate(app, db)

    # Register blueprint
    app.register_blueprint(courses_bp)

    # 404 handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    # 500 handler
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
