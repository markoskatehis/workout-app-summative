import os
from flask import Flask
from flask_migrate import Migrate
from .extensions import db

def create_app():
    app = Flask(__name__)

    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)

    db_path = os.path.join(instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    from .routes.exercises_routes import bp as exercise_bp
    from .routes.workout_routes import bp as workout_bp
    app.register_blueprint(exercise_bp)
    app.register_blueprint(workout_bp)

    return app