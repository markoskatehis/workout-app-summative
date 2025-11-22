#!/usr/bin/env python3

from app import create_app
from app.extensions import db
from models import Exercise, Workout, WorkoutExercise
from datetime import date

app = create_app()
with app.app_context():
    print("Deleting old data...")

    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()
    db.session.commit()

    print("Seeding exercises...")
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    db.session.add_all([pushup, squat, plank])
    db.session.commit()

    print("Seeding workouts...")
    today = date.today()
    workout1 = Workout(date=today, duration_minutes=45, notes="Upper body focus")
    workout2 = Workout(date=today, duration_minutes=30, notes="Lower body focus")
    db.session.add_all([workout1, workout2])
    db.session.commit()

    print("Linking exercises to workouts...")
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=pushup.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=plank.id, duration_seconds=60, sets=3)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=squat.id, reps=20, sets=3)
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete!")