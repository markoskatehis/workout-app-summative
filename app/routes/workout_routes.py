from flask import Blueprint, jsonify
from models import Workout, WorkoutExercise, Exercise
from app.schemas.workout_schema import workout_schema, workouts_schema

bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@bp.route("", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@bp.route("/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)

    exercises_info = []
    for we in workout.workout_exercises:
        exercises_info.append({
            "exercise_id": we.exercise.id,
            "name": we.exercise.name,
            "category": we.exercise.category,
            "equipment_needed": we.exercise.equipment_needed,
            "reps": we.reps,
            "sets": we.sets,
            "duration_seconds": we.duration_seconds
        })

    result = workout_schema.dump(workout)
    result["exercises"] = exercises_info

    return jsonify(result), 200