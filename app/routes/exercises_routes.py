from flask import Blueprint, jsonify
from models import Exercise, WorkoutExercise, Workout
from app.schemas.exercise_schema import exercise_schema, exercises_schema

bp = Blueprint("exercises", __name__, url_prefix="/exercises")

@bp.route("", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@bp.route("/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    associated_workouts = [
        we.workout for we in exercise.workout_exercises
    ]

    result = exercise_schema.dump(exercise)
    result["workouts"] = [
        {
            "id": w.id,
            "date": w.date.isoformat(),
            "duration_minutes": w.duration_minutes,
            "notes": w.notes
        } for w in associated_workouts
    ]

    return jsonify(result), 200