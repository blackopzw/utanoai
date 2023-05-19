import streamlit as st
import pandas as pd
import numpy as np
import csv

st.set_page_config(page_title="AI Dietician for Pregnant Women")

def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2
    return bmi

def get_weight_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_calories(weight, height, age, activity, trimester, medical_condition):
    bmr = 0
    if medical_condition == "None":
        if trimester == "First":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif trimester == "Second":
            bmr = 10 * weight + 6.25 * height - 5 * age + 10
        elif trimester == "Third":
            bmr = 10 * weight + 6.25 * height - 5 * age - 5
    else:
        if trimester == "First":
            bmr = 10 * weight + 6.25 * height - 5 * age - 10
        elif trimester == "Second":
            bmr = 10 * weight + 6.25 * height - 5 * age - 5
        elif trimester == "Third":
            bmr = 10 * weight + 6.25 * height - 5 * age - 15

    if activity == "Sedentary":
        calories = bmr * 1.2
    elif activity == "Lightly Active":
        calories = bmr * 1.375
    elif activity == "Moderately Active":
        calories = bmr * 1.55
    elif activity == "Very Active":
        calories = bmr * 1.725
    else:
        calories = bmr * 1.9

    return calories

def recommend_diet(calories):
    diets = pd.read_csv(r"C:\Users\victoria\Desktop\utanoaidiet\diets.csv")
    diets = diets.dropna(subset=["Diet_Name", "calories", "fats", "carbohydrates", "sugar", "vitamins", "protein"])
    diets = diets.sample(n=3)
    diet = []
    for i, row in diets.iterrows():
        diet.append(f"{row['Diet_Name']} ({row['calories']} calories, {row['fats']}g fats, {row['carbohydrates']}g carbohydrates, {row['sugar']}g sugar, {row['vitamins']}g vitamins, {row['protein']}g protein)")
    return ', '.join(diet)
    
def save_user_details(first_name, last_name, age, weight, height, trimester, medical_condition, activity, bmi, weight_status, calories, diet):
    with open('user.csv', mode='a', newline='') as user_file:
        writer = csv.writer(user_file)
        writer.writerow([first_name, last_name, age, weight, height, trimester, medical_condition, activity, bmi, weight_status, calories, diet])

def main():
    st.title("Utano AI Dietician")

    menu = ["Admin", "User"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "User":
        st.subheader("User")
        user_username = st.sidebar.text_input("User Username")
        user_password = st.sidebar.text_input("User Password", type="password")
        
        if st.sidebar.checkbox("Login"):
            if user_password == "user123":
                st.success("You Are Logged in")

            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            age = st.slider("Age", 18, 60, 25)
            weight = st.number_input("Weight (kg)", 40, 200, 60)
            height = st.number_input("Height (cm)", 100, 250, 160)
            trimester = st.selectbox("Trimester", ["First", "Second", "Third"])
            medical_condition = st.selectbox("Medical Condition", ["None", "Gestational Diabetes", "Preeclampsia"])
            activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

            register_button = st.button("Submit")
            if register_button:
                bmi = calculate_bmi(weight, height)
                weight_status = get_weight_status(bmi)
                calories = calculate_calories(weight, height, age, activity, trimester, medical_condition)
                diet = recommend_diet(calories)
                save_user_details(first_name, last_name, age, weight, height, trimester, medical_condition, activity, bmi, weight_status, calories, diet)
                st.success("Success")
                st.write("Name:", first_name, last_name)
                st.write("Age:", age)
                st.write("Weight:", weight, "kg")
                st.write("Height:", height, "cm")
                st.write("Trimester:", trimester)
                st.write("Medical Condition:", medical_condition)
                st.write("Activity Level:", activity)
                st.write("BMI:", bmi)
                st.write("Weight Status:", weight_status)
                st.write("Calories:", calories)
                st.write("Recommended Diet:", diet)
            
            
    elif choice == "Admin":
        st.subheader("Admin")
        admin_username = st.sidebar.text_input("Admin Username")
        admin_password = st.sidebar.text_input("Admin Password", type="password")

        if st.sidebar.checkbox("Login"):
            if admin_password == "admin123":
                st.success("You Are Logged In")
            # Load user data
                user_data = pd.read_csv("user.csv")
                st.write("Total Users:", len(user_data))
                st.write(user_data)
            else:
                st.error("Incorrect Admin username or password")

if __name__ == "__main__":
    main()