from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import WorkoutExercise
from app.schemas_pkg import WorkoutExerciseSchema

bp = Blueprint('workout_exercise', __name__, url_prefix='/workout_exercises')
schema = WorkoutExerciseSchema()
schemas = WorkoutExerciseSchema(many=True)

@bp.route('', methods=['GET'])
def get_all_workout_exercises():
    exercises = WorkoutExercise.query.all()
    return jsonify(schemas.dump(exercises)), 200

@bp.route('/<int:id>', methods=['GET'])
def get_workout_exercise(id):
    exercise = WorkoutExercise.query.get(id)
    if not exercise:
        return jsonify({"error": "WorkoutExercise not found"}), 404
    return jsonify(schema.dump(exercise)), 200

@bp.route('/<int:id>', methods=['PATCH'])
def update_workout_exercise(id):
    exercise = WorkoutExercise.query.get(id)
    if not exercise:
        return jsonify({"error": "WorkoutExercise not found"}), 404

    data = request.get_json()
    try:
        updated_exercise = schema.load(data, instance=exercise, partial=True)
        db.session.commit()
        return jsonify(schema.dump(updated_exercise)), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid data or constraint violation"}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_workout_exercise(id):
    exercise = WorkoutExercise.query.get(id)
    if not exercise:
        return jsonify({"error": "WorkoutExercise not found"}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"WorkoutExercise {id} deleted successfully"}), 200