#!/usr/bin/env python3

from app import create_app
from app.extensions import db
from models import Exercise, Workout, WorkoutExercise

app = create_app()
with app.app_context():
    print("=== Exercises ===")
    exercises = Exercise.query.all()
    for e in exercises:
        print(f"ID: {e.id}, Name: {e.name}, Category: {e.category}, Equipment Needed: {e.equipment_needed}")

    print("\n=== Workouts ===")
    workouts = Workout.query.all()
    for w in workouts:
        print(f"ID: {w.id}, Date: {w.date}, Duration: {w.duration_minutes} mins, Notes: {w.notes}")

    print("\n=== Workout Exercises ===")
    workout_exercises = WorkoutExercise.query.all()
    for we in workout_exercises:
        print(
            f"Workout ID: {we.workout_id}, Exercise ID: {we.exercise_id}, "
            f"Reps: {we.reps}, Sets: {we.sets}, Duration: {we.duration_seconds}"
        )