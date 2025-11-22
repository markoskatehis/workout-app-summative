import requests
from datetime import date

BASE_URL = "http://127.0.0.1:5555"

def test_create_exercise():
    payload = {
        "name": "Burpee",
        "category": "strength",
        "equipment_needed": False
    }
    r = requests.post(f"{BASE_URL}/exercises", json=payload)
    print("Create Exercise:", r.status_code, r.json())

    if r.status_code != 201:
        return None

    return r.json()["id"]

def test_create_workout():
    payload = {
        "date": str(date.today()),
        "duration_minutes": 40,
        "notes": "Full body workout"
    }

    r = requests.post(f"{BASE_URL}/workouts", json=payload)
    print("Create Workout:", r.status_code, r.json())
    return r.json()["id"]


def test_link_exercise_to_workout(workout_id, exercise_id):
    payload = {
        "reps": 12,
        "sets": 3
    }

    r = requests.post(
        f"{BASE_URL}/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json=payload
    )

    print("Link Exercise to Workout:", r.status_code, r.json())


if __name__ == "__main__":
    exercise_id = test_create_exercise()

    workout_id = test_create_workout()

    test_link_exercise_to_workout(workout_id, exercise_id)