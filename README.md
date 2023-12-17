# Lab Insight App
Welcome to the Lab Insight App! This application provides a comprehensive platform for generating and understanding blood test reports. Below is an overview of the project structure and key components.

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

## Getting Started
- Install the required libraries by running " pip install -r requirements.txt ".
- Run the main script "🔬_Lab_Insight.py" to start the Lab Insight App.

Happy analyzing! 🩸📊
