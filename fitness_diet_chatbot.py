import pandas as pd
import numpy as np
import streamlit as st

# Load datasets
mega_gym_data = pd.read_csv(r"C:\Users\PC7\Documents\work\ai (python)\fitness_bot\megaGymDataset.csv")
usda_data = pd.read_csv(r"C:\Users\PC7\Documents\work\ai (python)\fitness_bot\USDA.csv")



# Helper Functions
def calculate_bmr(height, weight, age, gender):
    """
    Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.
    """
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def adjust_calories(bmr):
    """
    Adjust calorie needs based on the user's Basal Metabolic Rate (BMR).
    """
    return bmr  # Just return BMR for simplicity, without modifying based on any goal.

def recommend_exercises(category=None, body_part=None):
    """
    Recommend exercises based on optional category and optional body part focus.
    """
    # Filter dataset based on category
    filtered_data = mega_gym_data.copy()

    # Filter by category (e.g., 'Strength', 'Cardio', etc.)
    if category and category != 'None':
        filtered_data = filtered_data[filtered_data['Type'].str.contains(category, case=False, na=False)]
    
    # Further filter by body part if specified
    if body_part:
        filtered_data = filtered_data[filtered_data['BodyPart'].str.contains(body_part, case=False, na=False)]
    
    # If no exercises match, return a message
    if filtered_data.empty:
        return pd.DataFrame({'Message': ['No exercises found for the selected category.']})
    
    return filtered_data[['Title', 'Desc']].head(5)

def recommend_foods(calorie_limit):
    """
    Recommend foods based on calorie limits.
    """
    return usda_data[usda_data['Calories'] <= calorie_limit][['Description', 'Calories', 'Protein', 'TotalFat']].head(5)

# Streamlit App Interface
st.title('Fitness and Diet Chatbot')

# User inputs
height = st.number_input('Enter your height (cm):', min_value=50, max_value=300, step=1)
weight = st.number_input('Enter your weight (kg):', min_value=10, max_value=300, step=1)
age = st.number_input('Enter your age:', min_value=1, max_value=120, step=1)
gender = st.selectbox('Select your gender:', ['Male', 'Female'])

# Process inputs and calculate BMR
bmr = calculate_bmr(height, weight, age, gender)
calories_needed = adjust_calories(bmr)

# New input for exercise category
exercise_category = st.selectbox('Select an exercise category:', 
                                 ['None', 'Strength', 'Plyometrics', 'Cardio', 'Stretching', 'Powerlifting', 
                                  'Strongman', 'Olympic Weightlifting'])

# Process inputs and provide recommendations
if st.button('Get Recommendations'):
    st.subheader('Your Recommended Calorie Intake:')
    st.write(f'{calories_needed:.2f} kcal/day')
    
    st.subheader('Recommended Exercises:')
    exercises = recommend_exercises(category=exercise_category)
    st.table(exercises)
    
    st.subheader('Recommended Foods:')
    foods = recommend_foods(calories_needed)
    st.table(foods)
