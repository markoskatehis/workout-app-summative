from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import Exercise
from app.extensions import db
from app.schemas_pkg import exercise_schema, exercises_schema

bp = Blueprint("exercises", __name__, url_prefix="/exercises")

@bp.route("", methods=["POST"])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return {"error": "No input data provided"}, 400

    try:
        data = exercise_schema.load(json_data)
    except Exception as e:
        return {"error": str(e)}, 400

    new_exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data["equipment_needed"]
    )

    db.session.add(new_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Exercise name must be unique"}, 400

    return exercise_schema.dump(new_exercise), 201

@bp.route("", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200

@bp.route("/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    associated_workouts = [we.workout for we in exercise.workout_exercises]

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

@bp.route("/<int:id>", methods=["PATCH"])
def update_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404

    json_data = request.get_json()
    if not json_data:
        return {"error": "No input data provided"}, 400

    if "name" in json_data:
        exercise.name = json_data["name"].strip() if json_data["name"] else exercise.name
    if "category" in json_data:
        exercise.category = json_data["category"].lower() if json_data["category"] else exercise.category
    if "equipment_needed" in json_data:
        exercise.equipment_needed = json_data["equipment_needed"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Exercise name must be unique"}, 400
    except ValueError as ve:
        db.session.rollback()
        return {"error": str(ve)}, 400
    except Exception as ex:
        db.session.rollback()
        return {"error": "Unexpected error: " + str(ex)}, 500

    return exercise_schema.dump(exercise), 200


@bp.route("/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404

    try:
        db.session.delete(exercise)
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        return {"error": "Could not delete exercise: " + str(ex)}, 500

    return {"message": f"Exercise {id} deleted successfully"}, 200