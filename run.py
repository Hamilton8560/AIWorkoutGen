
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import api

def configure():
    load_dotenv()

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv('OPENAI_API_KEY')



@app.route('/analyze-OSHA', methods=['POST'])
def analyze_OSHA():
    try:
        data = request.json
        data_prompt = data.get('prompt')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type":"json_object"},
            messages=[
                {"role":"system", "content":"You are a helpful assistant, specializing in OSHA regulations. Designed to output JSON."},
                {"role":"user", "content": data_prompt}
            ]
        )


        return jsonify(response.choices[0].message.content)

    except Exception as e:
        app.logger.error(f"Error: {e}")
    return jsonify({'error': str(e)}), 500
    
@app.route('/analyze-exercise', methods=['POST'])
def analyze_exercise():
    try:
        data = request.json
        exercise_name = data.get('exerciseName')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": f"Analyze the exercise {exercise_name} in JSON format and provide its agonists, synergists, jointMovements, and force."}
            ]
        )

        return jsonify(response.choices[0].message.content)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate-workout', methods=['POST'])
def generate_workout():
    try:
        
        data =request.json
        # workout_info=data.get('workoutInfo')#user inputs a workout description
        user_info = data.get('userInfo')# Assuming userInfo contains all necessary details
        available_exercises = data.get('availableExercises')  # List of exercises from your DB
        formatted_goals = ', '.join(user_info['goal']).replace('_', ' ').title()
        
        print({user_info['weight']})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            #model="gpt-4-1106-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": f"Create a workout plan for a {user_info['age']} year old {user_info['gender']} " \
                f"weighing {user_info['weight']} {user_info['weightUnit']}. Goals: {formatted_goals}. " \
                f"Max lifts: Deadlift {user_info['maxDeadlift']}{user_info['weightUnit']}, " \
                f"Squat {user_info['maxSquat']}{user_info['weightUnit']}, Bench Press {user_info['maxBench']}{user_info['weightUnit']}, " \
                f"Bentover Row {user_info['maxRow']}{user_info['weightUnit']}. Include a list of this information structued in JSON as workoutInfo: age,gender,weight,goals[], maxLifts object: "\
                f"deadlift, squat, benchPress, bentoverRow. Create a string in a few simple words, under focus that shows the primary focus of this workoutplan"\
                f" Provide workouts for {user_info['trainingDays']} days, listing each as day1, day2, etc, under workoutLog. This user is considered {user_info['experience']} so make the workout volume and complexity of exercises cater to that experience level."\
                f"Here is more workout information: {user_info['workoutInfo']}. Under day should be exercise1, exercise2, etc." \
                f"the exercises should include name, sets, reps, and weight:if unsure use percentage of max or bodyweight, assisted, or other miscellaneous descriptions, just the number and percent symbol. The exercises that are available to choose from are: {', '.join(available_exercises)}. " \
                f"include under nutritionRecommendations dailyCalories:total calories, dailyFats:grams, dailyCarbs:grams, dailyProtein:grams, percentFats, percentCarbs, percentProtein "\
                f"and a description of the diet under description. Give the workoutplan an original name under title, make it a catchy name."\
                f"include any exercises that should be added to available exercises that would improve this plan, under recommendedExercises. Under explanations explain why you chose everything for this workout and nutrition plan, and what is the best frequency per week and RPE for this type of lifter."\
                f"Format the plan in JSON."}   
            ]
        )
        
        
        return jsonify(response.choices[0].message.content)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    configure()
    app.run(debug=True, port=5000)
