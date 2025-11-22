from flask import Blueprint, request, jsonify
from app.extensions import db
from models import Workout, WorkoutExercise, Exercise
from app.schemas_pkg import workout_schema, workouts_schema
from datetime import date

bp = Blueprint("workouts", __name__, url_prefix="/workouts")

@bp.route("", methods=["POST"])
def create_workout():
    data = request.get_json()
    try:
        validated = workout_schema.load(data)
    except Exception as e:
        return {"error": str(e)}, 400

    workout = Workout(**validated)
    db.session.add(workout)
    db.session.commit()
    return workout_schema.dump(workout), 201

@bp.route("", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@bp.route("/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    exercises_info = [
        {
            "exercise_id": we.exercise.id,
            "name": we.exercise.name,
            "category": we.exercise.category,
            "equipment_needed": we.exercise.equipment_needed,
            "reps": we.reps,
            "sets": we.sets,
            "duration_seconds": we.duration_seconds
        } for we in workout.workout_exercises
    ]
    result = workout_schema.dump(workout)
    result["exercises"] = exercises_info
    return jsonify(result), 200

@bp.route("/<int:id>", methods=["PATCH"])
def update_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404

    json_data = request.get_json()
    if not json_data:
        return {"error": "No input data provided"}, 400

    if "date" in json_data:
        try:
            workout.date = date.fromisoformat(json_data["date"])
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400
    if "duration_minutes" in json_data:
        workout.duration_minutes = json_data["duration_minutes"]
    if "notes" in json_data:
        workout.notes = json_data["notes"]

    try:
        db.session.commit()
    except ValueError as ve:
        db.session.rollback()
        return {"error": str(ve)}, 400
    except Exception as ex:
        db.session.rollback()
        return {"error": "Unexpected error: " + str(ex)}, 500

    return workout_schema.dump(workout), 200

@bp.route("/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404

    try:
        db.session.delete(workout)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return {"error": "Could not delete workout: " + str(ex)}, 500

    return {"message": f"Workout {id} deleted successfully"}, 200