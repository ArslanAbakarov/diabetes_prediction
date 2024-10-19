from shiny import App, ui, reactive, render
import pandas as pd
from pycaret.classification import load_model
import numpy as np

# Load the model using PyCaret's load_model
model = load_model('model/diabetes_model')

# Define the UI
app_ui = ui.page_fluid(
    
    ui.HTML("""
        <link rel="stylesheet" href="https://fonts.cdnfonts.com/css/noto-sans">
    """),
    
      ui.tags.style("""
                    
        p {
            line-height: 33px !important;
        }
        
        .form-select {
            font-size: 20px !important;
        }
                    
        body {
            margin: 25px;
            line-height: 33px;
            font-size: 20px !important;
            font-family: 'Noto Sans', sans-serif !important;
        }
        
        .h1, .h2, .h3, .h4, .h5, .h6, h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
        
        
        container-fluid {
            padding: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        h1 {
            border-bottom: .18em solid #af3c43;
            -o-border-image: linear-gradient(to right, #af3c43 71px, transparent 71px);
            border-image: linear-gradient(to right, #af3c43 71px, transparent 71px);
            border-image-slice: 1;
            border-left-width: 0;
            border-right-width: 0;
            border-top-width: 0;
            margin-bottom: 30px !important;
        }
        
        h2 {
            margin-bottom: 40px !important;
        }
        
        #logoimage {
            height: 50px !important;
            margin-bottom: 30px;
        }
        
        .page-container {
            padding-top: 30px;
        }
        
        .prediction-label, .shiny-html-output {
            border-radius: 10px;
            padding: 20px;
            font-size: 1.5rem;
            background-color: white;
            margin-top: 20px;
            
            
            background-color: #f5f5f5;
            margin-bottom: 20px;
            padding: 24px;
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
        
        .introduction {
            margin-top: 40px;
            margin-bottom: 40px;
        }
        
        hr {
            height: 3px !important;
            color: black !important;
            width: 100%;
            border-color: black !important;
            background-color: black !important;
        }
        
        h2 {
            margin-bottom: 40px;
        }
        
        container {
            width: 970px
        }
        
        .irs--shiny .irs-handle {
            background-color: black;
        }
        
        .irs--shiny .irs-from, .irs--shiny .irs-to, .irs--shiny .irs-single {
            color: white !important;
            background-color: black !important;
        }
        
        .parameters-container {
            margin-bottom: 80px;
        }
        
        #predict {
            margin-top: 20px;
        }
        
        button {
            background-color: #26374a !important;
            border-color: #26374a !important;
            color: white !important;
            font-size: 20px !important;
        }
        
        .irs--shiny .irs-bar {
            background-color: black;
            height: 5px !important;
        }
        
        .form-label, .shiny-input-container .control-label {
            # margin-top: 10px;
        }
        
        .form-group {
            margin-bottom: 23px;
        }
        
    """),
      
    ui.tags.head(
        # Link to a Bootswatch theme (Cerulean)
        ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootswatch@5.1.0/dist/cerulean/bootstrap.min.css")
    ),
    
    # https://shiny.posit.co/py/api/core/ui.input_slider.html
    
    ui.div(
        
        ui.div(
            ui.output_image("logoimage"),
            class_="container",
        ),
        
        # output hr
        
        ui.hr(),
        
        ui.div (

            ui.h1("Diabetes Prescreening"),
            ui.p("The Public Health Agency of Canada is looking to undertake a Public Health campaign to target high risk individuals for Diabetes. The YorkU student team were hired to prepare a forecast model to help the Authority determine risk factors to diabetes. With these risk factors, the Public Health would better target their campaign to optimise spend and resources on the indivduals or groups most likely to be at risk."),
            class_="container introduction",
        
        ),
    
        ui.div(
            
            ui.div(
                    # ui.p("The model was developed using PyCaret’s classification module, which automates many of the preprocessing, model selection, and tuning steps. Various algorithms were tested, and the best-performing model was selected based on evaluation metrics such as accuracy, precision, recall, and F1-score. The final model is designed to predict whether an individual has diabetes (binary classification: Yes/No) based on the input features."),
                    class_="",
            ),
            
            ui.div (        
                    
                ui.h2("Please fill in the form:"),
                
                # Input fields for model features
                ui.input_slider("bmi", "BMI", 0.0, 100.0, value=3.029167),
                ui.input_slider("age", "AGE", 0.0, 80, value=16.0),
                ui.input_slider("HbA1c_level", "HbA1c Level", 0.0, 20.0, value=1.621879),
                ui.input_slider("blood_glucose_level", "Blood Glucose Level", 0.0, 200.0, value=5.062595),

                # https://shiny.posit.co/py/api/core/ui.input_select.html
                ui.input_select("hypertension", "Hypertension", ["Yes", "No"], selected="No"),
                ui.input_select("heart_desease", "Heart Desease", ["Yes", "No"], selected="No"),
                ui.input_select("smoking_history", "Smoking History", ["current", "never", "not current", "ever", "former"], selected="Never"),
                ui.input_select("gender", "Gender", ["Male", "Female", "Other"], selected="Female"),
                
                # Button to trigger prediction
                ui.input_action_button("predict", "Predict"),

                # Output the prediction
                # ui.output_text_verbatim("prediction"),
                ui.output_ui("prediction"),
                
                class_="parameters-container",
                
            ),
            
         
            
            class_="container",
        ),
        class_="page-container",
    )
)

# Define the server logic
def server(input, output, session):
    
    logoimg: dict = {
        "src": "sig-blk-en.svg",
        "height": "40px",
        "content_type": "image/svg+xml"  # Specify the type of the image, especially for SVG
    }


    # Define the prediction logic
    @output
    
    @render.image
    def logoimage():
        from pathlib import Path
        return logoimg

    
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
        # return f'Predicted Diabetes: {"At risk of developing diabetes." if predicted_class == 1 else "Not at risk of developing diabetes. Good job."} '
        
        if predicted_class == 1:
            return ui.HTML('<br><div class="prediction-label" style="color: red">Predicted: At risk of developing diabetes.</div>')
        else:
            return ui.HTML('<br><div class="prediction-label" style="color:green">Predicted: Not at risk of developing diabetes. <br></div>')
        # return f'Predicted Diabetes: {"At risk of developing diabetes." if predicted_class == 1 else "Not at risk of developing diabetes. Good job."} '
    

# Create the app object
app = App(app_ui, server)