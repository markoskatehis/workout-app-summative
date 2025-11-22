import requests
import json

BASE_URL = "http://127.0.0.1:5555"

def print_response(r):
    print(f"\nURL: {r.url}")
    print(f"Status Code: {r.status_code}")
    try:
        print("Response JSON:", json.dumps(r.json(), indent=2))
    except Exception:
        print("Response Text:", r.text)

def test_exercises():
    print("\n--- TEST: Exercises ---")

    r = requests.get(f"{BASE_URL}/exercises")
    print_response(r)

    new_ex = {"name": "Plank", "category": "strength", "equipment_needed": False}
    r = requests.post(f"{BASE_URL}/exercises", json=new_ex)
    print_response(r)
    exercise_id = r.json().get("id")

    r = requests.get(f"{BASE_URL}/exercises/{exercise_id}")
    print_response(r)

    patch_data = {"name": "Side Plank", "category": "mobility"}
    r = requests.patch(f"{BASE_URL}/exercises/{exercise_id}", json=patch_data)
    print_response(r)

    r = requests.delete(f"{BASE_URL}/exercises/{exercise_id}")
    print_response(r)


def test_workouts():
    print("\n--- TEST: Workouts ---")

    new_wk = {"date": "2025-11-22", "duration_minutes": 60, "notes": "Test workout"}
    r = requests.post(f"{BASE_URL}/workouts", json=new_wk)
    print_response(r)
    workout_id = r.json().get("id")

    r = requests.get(f"{BASE_URL}/workouts")
    print_response(r)

    r = requests.get(f"{BASE_URL}/workouts/{workout_id}")
    print_response(r)

    return workout_id


def test_workout_exercises(workout_id):
    print("\n--- TEST: Linking WorkoutExercises ---")

    r = requests.get(f"{BASE_URL}/exercises")
    exercises = r.json()
    if not exercises:
        print("No exercises available to link.")
        return
    exercise_id = exercises[0]["id"]

    link_data = {"reps": 10, "sets": 3, "duration_seconds": 60}
    r = requests.post(f"{BASE_URL}/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
                      json=link_data)
    print_response(r)


if __name__ == "__main__":
    test_exercises()

    workout_id = test_workouts()

    test_workout_exercises(workout_id)

    print("\n--- ALL TESTS COMPLETE ---")