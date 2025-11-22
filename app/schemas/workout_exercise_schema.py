from marshmallow import Schema, fields, validates_schema, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)

    sets = fields.Int()
    reps = fields.Int()
    duration_seconds = fields.Int()

    @validates_schema
    def validate_required_fields(self, data, **kwargs):
        sets = data.get("sets")
        reps = data.get("reps")
        duration = data.get("duration_seconds")

        if (reps is None or sets is None) and duration is None:
            raise ValidationError(
                "You must provide either reps/sets OR duration_seconds."
            )

        if reps is not None and reps <= 0:
            raise ValidationError("Reps must be a positive integer.")

        if sets is not None and sets <= 0:
            raise ValidationError("Sets must be a positive integer.")

        if duration is not None and duration <= 0:
            raise ValidationError("Duration must be positive.")

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)