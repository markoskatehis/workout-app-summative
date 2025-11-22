from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models import Workout
from app.extensions import db
from app.schemas_pkg import workout_schema, workouts_schema
from datetime import datetime

bp = Blueprint("workouts", __name__, url_prefix="/workouts")

@bp.route("", methods=["POST"])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return {"error": "No input data provided"}, 400

    try:
        data = workout_schema.load(json_data)
    except Exception as e:
        return {"error": str(e)}, 400

    workout_date = data.get("date")
    if isinstance(workout_date, str):
        try:
            workout_date = datetime.fromisoformat(workout_date).date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400

    new_workout = Workout(
        date=workout_date,
        duration_minutes=data.get("duration_minutes", 0),
        notes=data.get("notes", "")
    )

    db.session.add(new_workout)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Could not create workout due to database error"}, 400

    return workout_schema.dump(new_workout), 201

@bp.route("", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@bp.route("/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return jsonify(workout_schema.dump(workout)), 200

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
            workout.date = datetime.fromisoformat(json_data["date"]).date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400
    if "duration_minutes" in json_data:
        workout.duration_minutes = json_data["duration_minutes"]
    if "notes" in json_data:
        workout.notes = json_data["notes"]

    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return {"error": "Could not update workout: " + str(ex)}, 500

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