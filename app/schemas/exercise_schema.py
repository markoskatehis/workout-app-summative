from marshmallow import Schema, fields, validate, ValidationError, validates


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=50)
    )

    equipment_needed = fields.Bool(required=True)

    @validates("name")
    def validate_name_not_blank(self, value):
        if not value.strip():
            raise ValidationError("Exercise name cannot be blank.")

    @validates("category")
    def validate_category(self, value):
        if not value.strip():
            raise ValidationError("Category cannot be blank.")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)