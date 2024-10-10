from shiny import App, ui, reactive, render
import pandas as pd
from pycaret.classification import load_model
import numpy as np

# Load the model using PyCaret's load_model
model = load_model('model/diabetes_model')

# Define the UI
app_ui = ui.page_fluid(
    
      ui.tags.style("""
        body {
            margin: 25px;
            font-size: 16px;
        }
        #prediction {
            margin-top: 20px;
            padding: 20px;
            font-size: 1.5rem;
        }
        
        select {
            border-radius: 10px;
            font-size: 1.5rem;
            
        }
        
        .irs-line {
            border-width: 1px;
            border-style: solid;
        }
        
        .shiny-input-container:not(.shiny-input-container-inline) {
            width: 600px;
        }
        
        .irs--shiny .irs-min, .irs--shiny .irs-max {
            font-size: 1rem;
        }
        
        .irs--shiny .irs-from, .irs--shiny .irs-to, .irs--shiny .irs-single {
            font-size: 1rem;
            top: -10px !important;
        }
        
        .control-label {
            font-size: 1.5rem;
        }
        
        .form-select {
            font-size: 1.5rem;
        }
        
        .custom-container {
            display: flex;
            justify-content: left;
        }
        
        .settings {
            border-radius: 20px;
            background-color: #f0f0f0;
            padding: 20px;            
        }
        
        .sidebar {
            flex: 1;
            margin-left: 30px;
            padding: 30px;
            background-color: #f0f0f0;
            border-radius: 10px;
        }
        
        h2 {
            margin-bottom: 40px;
            }
    """),
    
    # https://shiny.posit.co/py/api/core/ui.input_slider.html
    
    ui.div(

        ui.div (        
            ui.h2("Diabetes Prediction, Group 1, Fall of 2024"),
            
            # Input fields for model features
            ui.input_slider("bmi", "BMI", 0.0, 100.0, value=3.029167),
            ui.input_slider("age", "AGE", 0.0, 80, value=16.0),
            ui.input_slider("HbA1c_level", "HbA1c Level", 0.0, 20.0, value=1.621879),
            ui.input_slider("blood_glucose_level", "Blood Glucose Level", 0.0, 200.0, value=5.062595),

            # https://shiny.posit.co/py/api/core/ui.input_select.html
            ui.input_select("hypertension", "Hypertension", ["Yes", "No"], selected="No"),
            ui.input_select("heart_desease", "Heart Desease", ["Yes", "No"], selected="No"),
            ui.input_select("smoking_history", "Smoking History", ["No Info", "current", "never", "not current", "ever", "former"], selected="Never"),
            ui.input_select("gender", "Gender", ["Male", "Female", "Other"], selected="Female"),
            
            # Button to trigger prediction
            ui.input_action_button("predict", "Predict"),

            # Output the prediction
            ui.output_text_verbatim("prediction"),
            class_="settings"
            
        ),
        
        ui.div(
                ui.h3("Project Description [PLACEHOLDER DESCRIPTION]"),
                ui.p("This project involves the development of a machine learning model aimed at predicting the likelihood of diabetes in individuals based on key health features. The model was trained using a diabetes dataset that includes demographic information, medical history, and relevant health metrics. The objective of this model is to assist healthcare professionals or individuals in assessing the risk of diabetes, potentially enabling early intervention and lifestyle adjustments to mitigate the risk."),
                ui.h3("Dataset"),
                ui.p("The dataset consists of records of patients with the following features:"),
                ui.h3("Model"),
                ui.p("The model was developed using PyCaret’s classification module, which automates many of the preprocessing, model selection, and tuning steps. Various algorithms were tested, and the best-performing model was selected based on evaluation metrics such as accuracy, precision, recall, and F1-score. The final model is designed to predict whether an individual has diabetes (binary classification: Yes/No) based on the input features."),
                class_="sidebar",
        ),
        
        class_="custom-container"
    )
)

# Define the server logic
def server(input, output, session):
    # Define the prediction logic
    @output
    @render.text
    def prediction():
        # Wait until the button is clicked
        if input.predict() == 0:
            return "Click 'Predict' to get the result."
        
        genderFemale = 0 
        genderMale = 0
        genderOther = 0
        
        if input.gender() == "Male":
            genderFemale = 0
            genderMale = 1
            genderOther = 0
            
        if input.gender() == "Female":
            genderFemale = 1
            genderMale = 0
            genderOther = 0
            
        if input.gender() == "Other":
            genderFemale = 0
            genderMale = 0
            genderOther = 1
            
            
        smokingNoInfo = 0
        smokingCurrent = 0
        smokingEver = 0
        smokingFormer = 0
        smokingNever = 0
        smokingNotCurrent = 0
        
        if input.smoking_history() == "No Info":
            smokingNoInfo = 1
            smokingCurrent = 0
            smokingEver = 0
            smokingFormer = 0
            smokingNever = 0
            smokingNotCurrent = 0
        
        if input.smoking_history() == "current":
            smokingNoInfo = 0
            smokingCurrent = 1
            smokingEver = 0
            smokingFormer = 0
            smokingNever = 0
            smokingNotCurrent = 0
        
        if input.smoking_history() == "ever":
            smokingNoInfo = 0
            smokingCurrent = 0
            smokingEver = 1
            smokingFormer = 0
            smokingNever = 0
            smokingNotCurrent = 0
        
        if input.smoking_history() == "former":
            smokingNoInfo = 0
            smokingCurrent = 0
            smokingEver = 0
            smokingFormer = 1
            smokingNever = 0
            smokingNotCurrent = 0
        
        if input.smoking_history() == "never":
            smokingNoInfo = 0
            smokingCurrent = 0
            smokingEver = 0
            smokingFormer = 0
            smokingNever = 1
            smokingNotCurrent = 0
        
        if input.smoking_history() == "not current":
            smokingNoInfo = 0
            smokingCurrent = 0
            smokingEver = 0
            smokingFormer = 0
            smokingNever = 0
            smokingNotCurrent = 1
            
        heart_disease = 0
        hypertension = 0
        
        if input.heart_desease() == "Yes":
            heart_disease = 1
        else:
            heart_disease = 0
            
        if input.hypertension() == "Yes":
            hypertension = 1
        else:
            hypertension = 0
            
        
        # Create a DataFrame with all required features, including one-hot encoded categories
        features = pd.DataFrame({
            'age': [input.age()],
            'hypertension': [hypertension],  # Placeholder, add input fields for these if needed
            'heart_disease': [heart_disease],
            'bmi': [input.bmi()],
            'HbA1c_level': [input.HbA1c_level()],  # Placeholder value
            'blood_glucose_level': [input.blood_glucose_level()],  # Placeholder value
            
            # One-hot encoded 'smoking_history' columns
            'smoking_history_No Info': [smokingNoInfo],  # Example: assuming 'No Info' is selected
            'smoking_history_current': [smokingCurrent],
            'smoking_history_ever': [smokingEver],
            
            'smoking_history_former': [smokingFormer],
            'smoking_history_never': [smokingNever],
            'smoking_history_not current': [smokingNotCurrent],
            
            # One-hot encoded 'gender' columns
            'gender_Female': [genderFemale],  # Example: assuming the user is female
            'gender_Male': [genderMale],
            'gender_Other': [genderOther]
        })

        # Make prediction using the pre-trained model
        # trained_model = model.steps[-1][1]
        predicted_class = model.predict(features)[0]
        
        # Return the predicted class
        return f'Predicted Diabetes: {"Yes" if predicted_class == 1 else "No"} '

# Create the app object
app = App(app_ui, server)