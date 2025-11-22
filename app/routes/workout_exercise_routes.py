from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Workout, Exercise, WorkoutExercise
from app.schemas_pkg.workout_exercise_schema import workout_exercise_schema, workout_exercises_schema

bp = Blueprint("workout_exercise", __name__, url_prefix="/workouts")

@bp.route("/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return {"error": f"Workout {workout_id} not found"}, 404

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return {"error": f"Exercise {exercise_id} not found"}, 404

    json_data = request.get_json()
    if not json_data:
        return {"error": "No input data provided"}, 400

    reps = json_data.get("reps")
    sets = json_data.get("sets")
    duration_seconds = json_data.get("duration_seconds")

    new_we = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=reps,
        sets=sets,
        duration_seconds=duration_seconds
    )

    db.session.add(new_we)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "WorkoutExercise could not be created (duplicate or invalid data)"}, 400
    except Exception as ex:
        db.session.rollback()
        return {"error": "Unexpected error: " + str(ex)}, 500

    return workout_exercise_schema.dump(new_we), 201

@bp.route("/workout_exercises", methods=["GET"])
def get_all_workout_exercises():
    all_we = WorkoutExercise.query.all()
    return jsonify(workout_exercises_schema.dump(all_we)), 200

@bp.route("/workout_exercises/<int:id>", methods=["DELETE"])
def delete_workout_exercise(id):
    we = WorkoutExercise.query.get(id)
    if not we:
        return {"error": "WorkoutExercise not found"}, 404

    try:
        db.session.delete(we)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return {"error": "Could not delete WorkoutExercise: " + str(ex)}, 500

    return {"message": f"WorkoutExercise {id} deleted successfully"}, 200