# Lab Insight App

## Abstract
The Lab Insight App is a comprehensive tool designed to facilitate the understanding and interpretation of blood test results. This project addresses the need for a user-friendly interface that empowers both patients and medical professionals to explore, analyze, and generate informative reports based on blood test measures.

## Background and Problem Statement
Interpreting blood test results can be challenging for individuals without a medical background. Patients often struggle to comprehend the significance of various measures, while medical professionals need efficient tools to generate detailed reports for their patients. The Lab Insight App aims to bridge this gap by providing a user-friendly platform that translates complex blood test data into easily understandable reports.

## Impact and Proposed Solution
The Lab Insight App has a significant impact on healthcare by:
- Empowering Patients: Patients can input their blood test results, receive detailed explanations, and make informed decisions about their health.
- Assisting Medical Professionals: Healthcare practitioners can use the app to generate professional reports quickly, enhancing communication with patients.
- Enhancing Healthcare Accessibility: The app's user-friendly interface makes it accessible to a broader audience, promoting health literacy.
The proposed solution involves leveraging natural language processing through LangChain for searching and interpreting blood test measures. The app ensures data privacy by not persisting any user data beyond the app's session.

## Files
### 🔬 Lab_Insight.py
This is the main script for the Lab Insight App. It serves as the home page where users can search for blood test measures. The app utilizes LangChain to search for measures, and upon finding a match, it displays additional information. The script integrates with the data.csv file to retrieve information about available blood test measures and their units.

### 📁 data.csv
This CSV file contains a list of available blood test measures in the app, along with their corresponding units. This data is used by the Lab_Insight.py script to provide users with detailed information.

### 📁 pages
This directory contains individual scripts for different pages in the app:

- 📇 Patient_Insight.py: This page allows patients to input their blood analysis results. The app generates a report explaining the results in a patient-friendly manner.

- 🩺 MedPro_Insight.py: Similar to the patient page, this page is designed for medical professionals. The generated report is more detailed and tailored for healthcare practitioners.

- ℹ️ Source_Details.py: This page provides details about data sources, references, and privacy information. It serves as an informational hub for users seeking more insights into the app's data and its handling.

### 📁 persist_db
This directory contains the Chroma Vector Database, a key component for enhancing the functionality of the app.

### 📝 preprocess.ipynb
This Jupyter Notebook contains the code for creating the Chroma Vector Database in the persist_db directory. It outlines the preprocessing steps to set up and maintain this crucial database.

### 📋 requirements.txt
This file lists the necessary libraries and dependencies required to run the Lab Insight App. Ensure you install these libraries before running the application.

## Instructions
### Prerequisites
Ensure you have Python installed on your machine.

### Setup
Clone this repository:
``` git clone https://github.com/your-username/lab-insight-app.git ```

Navigate to the project directory:
``` cd lab-insight-app ```

Install the required libraries:
``` pip install -r requirements.txt ```

### Running the App
Run the main script:

``` python 🔬_Lab_Insight.py ``` 
