import requests
from datetime import date

BASE_URL = "http://127.0.0.1:5555"

def test_create_exercise():
    payload = {
        "name": f"Burpee-{int(date.today().strftime('%s'))}",
        "category": "strength",
        "equipment_needed": False
    }
    url = f"{BASE_URL}/exercises"
    r = requests.post(url, json=payload)
    print("Create Exercise:", r.status_code, r.text)

    try:
        return r.json().get("id")
    except Exception:
        print("Failed to parse JSON for exercise creation.")
        return None

def test_create_workout():
    payload = {
        "date": str(date.today()),
        "duration_minutes": 40,
        "notes": "Full body workout"
    }
    url = f"{BASE_URL}/workouts"
    r = requests.post(url, json=payload)
    print("Create Workout:", r.status_code, r.text)

    try:
        return r.json().get("id")
    except Exception:
        print("Failed to parse JSON for workout creation.")
        return None

def test_link_exercise_to_workout(workout_id, exercise_id):
    payload = {
        "workout_id": workout_id,
        "exercise_id": exercise_id,
        "reps": 12,
        "sets": 3
    }
    url = f"{BASE_URL}/workout_exercises"
    r = requests.post(url, json=payload)
    print("Link Exercise to Workout:", r.status_code, r.text)

    try:
        return r.json().get("id")
    except Exception:
        print("Failed to parse JSON for linking exercise to workout.")
        return None

if __name__ == "__main__":
    exercise_id = test_create_exercise()
    if exercise_id is None:
        print("Exercise creation failed. Exiting.")
        exit(1)

    workout_id = test_create_workout()
    if workout_id is None:
        print("Workout creation failed. Exiting.")
        exit(1)

    link_id = test_link_exercise_to_workout(workout_id, exercise_id)
    if link_id:
        print(f"Successfully linked exercise {exercise_id} to workout {workout_id} with link id {link_id}")
    else:
        print("Linking exercise to workout failed.")