# Import necessary libraries
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import pandas as pd
import os 

os.environ['OPENAI_API_KEY'] = "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"

if "page" not in st.session_state :
    st.session_state.page = 0

def next():
    st.session_state.page = st.session_state.page + 1


persist_dir = "./persist_db/"

# Load the Excel file with field, subfield, measure, etc.
excel_file_path = "./data.csv"
df = pd.read_csv(excel_file_path, sep=";")

# Streamlit app layout
def main():
    st.title("Lab Report")
    
    if st.session_state.page == 0 :
        # User information form
        with st.form("user_info_form"):

            st.subheader("User Information / Analysis Options:")
            # Radio input for sex
            st.session_state.sex = st.radio("Select Sex:", ["Male", "Female"])

            # Numeric input for age
            st.session_state.age = st.number_input("Enter Age:", min_value=1, value=10, max_value=100)

            # Multi-select for Biochemistry
            st.session_state.biochemistry_options = st.multiselect("Select Biochemistry Analysis:", df[df["field"] == "BIOCHEMISTRY"]["mesure"])

            # Multi-select for Hematology
            #hematology_options = st.multiselect("Select Hematology Analysis:", df[df["field"] == "Hematology"]["subfield"])

            submit_button = st.form_submit_button("Next")

            if submit_button:
                # Display the form with selected options
                next()

    if st.session_state.page == 1 :

        # User information form
        with st.form("user_result"):
            
            st.subheader("Enter Analysis result:")

            # Display form for selected Biochemistry options
            display_numeric_form(st.session_state.biochemistry_options, "BIOCHEMISTRY")

            # Display form for selected Hematology options
            #display_numeric_form(hematology_options, "Hematology")
            generate_button = st.form_submit_button("Generate Report")

            if generate_button:
                # Generate report using PALM
                generate_report()
                

# Function to display numeric input form
def display_numeric_form(selected_options, section):

    st.subheader(f"{section} Analysis:")
    st.session_state.result = {}
    for option in selected_options:
        row = df[(df["field"] == section) & (df["mesure"] == option)].iloc[0]
        unit = row["unit"] if "unit" in df.columns else ""

        # Create numeric input for each selected option
        value = st.number_input(f"{option} ({unit})", min_value=0.0, key=f"{section}_{option}")
        st.session_state.result[option] = f"{option} = {value} {unit}"



# Function to generate a report using PALM
def generate_report():
    vectordb = None
    embedding = OpenAIEmbeddings()
    st.subheader("Generating report")
    for mesure in st.session_state.result.keys() : 
        
        query = f"""write the interpretation of the terms in the following blood "{st.session_state.result[mesure]}"/
                and explain the in detail its meanings."""
        
        section = df[df["mesure"] == mesure]["section"]
        vectordb = Chroma(embedding_function = embedding,
                        persist_directory = f"{persist_dir}BIOCHEMISTRY/{section}")

        chain = RetrievalQA.from_chain_type(llm = OpenAI(),
                                            retriever = vectordb.as_retriever(),
                                            chain_type="stuff")
        generated_text = chain.run(query)
        st.write(mesure)
        st.markdown(generated_text)
    

# Run the Streamlit app
if __name__ == "__main__":
    main()
