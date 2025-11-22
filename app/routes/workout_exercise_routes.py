# routes/workout_exercise_routes.py
from flask import Blueprint, request, jsonify
from sqlalchemy import exc

from models import db, Workout, Exercise, WorkoutExercise
from app.schemas.workout_exercise_schema import workout_exercise_schema

bp = Blueprint("workout_exercises", __name__, url_prefix="/workouts")


@bp.route("/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    w = Workout.query.get(workout_id)
    if not w:
        return jsonify({"error": "Workout not found"}), 404

    e = Exercise.query.get(exercise_id)
    if not e:
        return jsonify({"error": "Exercise not found"}), 404

    payload = request.get_json() or {}
    payload["workout_id"] = workout_id
    payload["exercise_id"] = exercise_id

    try:
        data = workout_exercise_schema.load(payload)
    except Exception as ve:
        return jsonify({"error": getattr(ve, "messages", str(ve))}), 400

    try:
        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds"),
        )
        db.session.add(we)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 400

    resp = {
        "id": we.id,
        "workout_id": we.workout_id,
        "exercise_id": we.exercise_id,
        "reps": we.reps,
        "sets": we.sets,
        "duration_seconds": we.duration_seconds,
    }
    return jsonify(resp), 201