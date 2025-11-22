from app import create_app
from app.extensions import db
from app.routes.exercises_routes import bp as exercise_bp
from app.routes.workout_routes import bp as workout_bp
from app.routes.workout_exercise_routes import bp as workout_exercise_bp
from flask_migrate import Migrate

app = create_app()

app.register_blueprint(exercise_bp)
app.register_blueprint(workout_bp)
app.register_blueprint(workout_exercise_bp)

migrate = Migrate(app, db)

@app.route("/", methods=["GET"])
def index():
    return {"message": "Workout API running"}, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)