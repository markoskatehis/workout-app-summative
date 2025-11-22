from flask import Flask
from .extensions import db, migrate
from .models import Exercise, Workout, WorkoutExercise
from .routes.exercises_routes import bp as exercises_bp
from .routes.workout_routes import bp as workouts_bp
from .routes.workout_exercise_routes import bp as workout_exercise_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(exercises_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(workout_exercise_bp)

    return app