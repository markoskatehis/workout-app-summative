# Workout Tracker API

## Project Description
Workout Tracker API is a RESTful service for managing workouts and exercises. Users can create exercises, create workouts, link exercises to workouts, and track reps, sets, and duration. Built with Flask, SQLAlchemy, and Marshmallow, it features full CRUD functionality, schema validations, and properly defined relationships.

## Installation

1. 
- Clone the repository
- Install dependencies with Pipenv using pipenv install
- Activate the pipenv shell

2.
Set up the database:

flask db init
flask db migrate
flask db upgrade

3.
Seed the database with starter data using flask shell:

flask shell
>>> from app.seed.seed_data import seed_data
>>> seed_data()

4.
To run the API, start the Flask server:

flask run --port 5555

The API will be available at http://127.0.0.1:5555/.


# API Endpoints
## Exercises

GET /exercises
	- List all exercises.

GET /exercises/<id>
	- Retrieve a single exercise along with associated workouts.

POST /exercises
	- Create a new exercise. Requires JSON payload:

	{
  	"name": "Push-up",
  	"category": "strength",
  	"equipment_needed": true
	}


PATCH /exercises/<id>
	- Update an existing exercise. Send any fields to update.

DELETE /exercises/<id>
	- Delete an exercise. Associated WorkoutExercises will also be removed.

## Workouts

GET /workouts
	- List all workouts.

GET /workouts/<id>
	- Retrieve a single workout with associated exercises and their reps/sets/duration.

POST /workouts
	- Create a new workout. Requires JSON payload:

	{
  	"date": "2025-11-22",
  	"duration_minutes": 45,
  	"notes": "Morning workout"
	}


DELETE /workouts/<id>
	- Delete a workout. Associated WorkoutExercises will also be removed.

## WorkoutExercises

POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
	- Add an exercise to a workout, including reps, sets, and duration. Requires JSON payload:

	{
  	"reps": 10,
  	"sets": 3,
  	"duration_seconds": 60
	}


## Notes

- All endpoints return JSON responses.

- Schema validations ensure proper data types and constraints (e.g., exercise name length, valid category, boolean for equipment_needed).

- Relationships:

	- An Exercise has many Workouts through WorkoutExercises.

	- A Workout has many Exercises through WorkoutExercises.

	- WorkoutExercises store reps, sets, and duration for each exercise in a workout.

- Table constraints and model validations are implemented to enforce uniqueness and proper data integrity.

## Development & Git Workflow

- Code is highly modular with clear separation of concerns.

- All migrations are tracked with Flask-Migrate.

- Seed file provides starter data for testing and development.
