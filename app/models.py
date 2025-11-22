
from app.extensions import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
from datetime import date

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value.lower() not in ["strength", "cardio", "mobility", "hypertrophy"]:
            raise ValueError("Category must be one of: strength, cardio, mobility, hypertrophy.")
        return value.lower()

    __table_args__ = (
        UniqueConstraint("name", name="uq_exercise_name"),
    )


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete"
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    __table_args__ = (
        CheckConstraint("reps >= 0", name="check_reps_non_negative"),
        CheckConstraint("sets >= 0", name="check_sets_non_negative"),
        CheckConstraint("duration_seconds >= 0", name="check_duration_non_negative"),
        UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise_pair"),
    )

    @validates("reps", "sets", "duration_seconds")
    def validate_numeric_fields(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be non-negative.")
        return value