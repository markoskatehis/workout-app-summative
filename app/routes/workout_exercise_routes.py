from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from models import Workout, Exercise, WorkoutExercise

bp = Blueprint("workout_exercises", __name__, url_prefix="/workout_exercises")

@bp.route("", methods=["POST"])
def add_exercise_to_workout():
    data = request.get_json() or {}

    workout_id = data.get("workout_id")
    exercise_id = data.get("exercise_id")
    reps = data.get("reps")
    sets = data.get("sets")
    duration_seconds = data.get("duration_seconds")

    if not workout_id or not exercise_id:
        return jsonify({"error": "workout_id and exercise_id are required"}), 400

    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    if ((reps is None or sets is None) and duration_seconds is None):
        return jsonify({"error": "You must provide either reps/sets OR duration_seconds"}), 400

    try:
        new_we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=reps,
            sets=sets,
            duration_seconds=duration_seconds
        )
        db.session.add(new_we)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "This exercise is already linked to the workout"}), 400
    except ValueError as ve:
        db.session.rollback()
        return jsonify({"error": str(ve)}), 400
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": "Unexpected error: " + str(ex)}), 500

    return jsonify({
        "id": new_we.id,
        "workout_id": new_we.workout_id,
        "exercise_id": new_we.exercise_id,
        "reps": new_we.reps,
        "sets": new_we.sets,
        "duration_seconds": new_we.duration_seconds
    }), 201