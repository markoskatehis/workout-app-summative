from flask import Blueprint, request, jsonify
from app.extensions import db
from models import Workout, WorkoutExercise, Exercise
from app.schemas_pkg import workout_schema, workouts_schema

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