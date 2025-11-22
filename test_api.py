import requests
from datetime import date

BASE_URL = "http://127.0.0.1:5555"

def create_exercise(name, category, equipment_needed=False):
    payload = {
        "name": name,
        "category": category,
        "equipment_needed": equipment_needed
    }
    r = requests.post(f"{BASE_URL}/exercises", json=payload)
    try:
        data = r.json()
    except Exception:
        data = {"error": "Invalid JSON response"}
    print(f"Create Exercise '{name}':", r.status_code, data)
    return data.get("id")


def create_workout(notes="Workout", duration=45):
    payload = {
        "date": str(date.today()),
        "duration_minutes": duration,
        "notes": notes
    }
    r = requests.post(f"{BASE_URL}/workouts", json=payload)
    try:
        data = r.json()
    except Exception:
        data = {"error": "Invalid JSON response"}
    print(f"Create Workout '{notes}':", r.status_code, data)
    return data.get("id")


def patch_workout(workout_id, duration=None, notes=None):
    payload = {}
    if duration is not None:
        payload["duration_minutes"] = duration
    if notes is not None:
        payload["notes"] = notes
    r = requests.patch(f"{BASE_URL}/workouts/{workout_id}", json=payload)
    try:
        data = r.json()
    except Exception:
        data = {"error": "Invalid JSON response"}
    print(f"Patch Workout {workout_id}:", r.status_code, data)

def delete_workout(workout_id):
    r = requests.delete(f"{BASE_URL}/workouts/{workout_id}")
    try:
        data = r.json()
    except Exception:
        data = {"error": "Invalid JSON response"}
    print(f"Delete Workout {workout_id}:", r.status_code, data)

def link_exercise_to_workout(workout_id, exercise_id, reps=None, sets=None, duration_seconds=None):
    payload = {}
    if reps is not None:
        payload["reps"] = reps
    if sets is not None:
        payload["sets"] = sets
    if duration_seconds is not None:
        payload["duration_seconds"] = duration_seconds

    r = requests.post(f"{BASE_URL}/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises", json=payload)
    try:
        data = r.json()
    except Exception:
        data = {"error": "Invalid JSON response"}
    print(f"Link Exercise {exercise_id} to Workout {workout_id}:", r.status_code, data)

if __name__ == "__main__":
    exercise_ids = []
    for name, category in [("Push-Up", "strength"), ("Burpee", "strength"), ("Jumping Jacks", "cardio")]:
        ex_id = create_exercise(name, category)
        if ex_id:
            exercise_ids.append(ex_id)

    workout_ids = []
    for i, notes in enumerate(["Morning workout", "Evening workout"], 1):
        w_id = create_workout(notes=notes, duration=30 + i*10)
        if w_id:
            workout_ids.append(w_id)

    for w_id in workout_ids:
        for ex_id in exercise_ids:
            link_exercise_to_workout(w_id, ex_id, reps=10, sets=2)

    for w_id in workout_ids:
        patch_workout(w_id, duration=60, notes="Updated workout")

    for w_id in workout_ids:
        delete_workout(w_id)