from marshmallow import Schema, fields, validate, ValidationError, validates
from app.schemas.workout_exercise_schema import WorkoutExerciseSchema


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=1000)
    )

    notes = fields.Str()

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema),
        dump_only=True
    )

    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be a positive number.")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)