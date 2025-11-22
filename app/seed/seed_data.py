from app.extensions import db
from app.models import Exercise, Workout, WorkoutExercise
from datetime import date

def seed_data():
    print("Deleting old data...")
    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()
    db.session.commit()

    print("Seeding exercises...")
    e1 = Exercise(name="Push-up", category="strength", equipment_needed=False)
    e2 = Exercise(name="Squat", category="strength", equipment_needed=False)
    e3 = Exercise(name="Running", category="cardio", equipment_needed=False)
    db.session.add_all([e1, e2, e3])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(date=date.today(), duration_minutes=30, notes="Morning workout")
    w2 = Workout(date=date.today(), duration_minutes=45, notes="Evening workout")
    db.session.add_all([w1, w2])
    db.session.commit()

    print("Linking exercises to workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e3.id)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e2.id)
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete!")