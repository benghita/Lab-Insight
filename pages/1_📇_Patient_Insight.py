# Import necessary libraries
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import pandas as pd
from fpdf import FPDF

# page configuration
st.set_page_config(
   page_title="Lab Insight",
   page_icon="🔬",
   initial_sidebar_state="expanded",
)

# Initialization of page variabal and functions
if "page" not in st.session_state : 
    st.session_state.page = 0

def next():
    st.session_state.page = st.session_state.page + 1

def back():
    st.session_state.page = st.session_state.page - 1

def reset():
    st.session_state.page = 0

persist_dir = "./persist_db/"

# Load the Excel file with field, subfield, measure, etc.
excel_file_path = "./data.csv"
df = pd.read_csv(excel_file_path, sep=";")

# Function to display numeric input form
def display_numeric_form(selected_options, section):

    result = {}
    for option in selected_options:

        row = df[(df["field"] == section) & (df["mesure"] == option)].iloc[0]
        unit = row["unit"] if "unit" in df.columns else ""

        # Create numeric input for each selected option
        value = st.number_input(f"{option} ({unit})", min_value=0.0, key=f"{section}_{option}")
        result[option] = f"{option} = {value} {unit}"
        
    return result

# Function to generate and save a report using GPT-3.5-turbo
def generate_report():

    # Define embedding
    embedding = OpenAIEmbeddings()

    # Initialize a FPDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=50)
    pdf.add_page()
    pdf.set_font("times", size=25, style='B')
    pdf.multi_cell(0, 10, "Generated Report : ", 0, 0, 'C')

    st.subheader("Generated Report")

    report = []

    if "report" not in st.session_state :
        for mesure in st.session_state.result.keys() : 
            
            # Define and run prompt
            query = f"""write the interpretation of the terms in the following blood "{st.session_state.result[mesure]}"/
                    and explain the in detail its meanings."""
            
            section = df[df["mesure"] == mesure]["section"]
            vectordb = Chroma(embedding_function = embedding,
                              persist_directory = f"{persist_dir}BIOCHEMISTRY/{section}")

            chain = RetrievalQA.from_chain_type(llm = OpenAI(),
                                                retriever = vectordb.as_retriever(),
                                                chain_type="stuff")
            generated_text = chain.run(query)

            subheader = f"- {mesure} :"
            # Save report
            report.append(subheader)
            report.append(generated_text)

            # Print results
            st.write(subheader)
            st.markdown(generated_text)
            
            # Save in fpdf object
            pdf.set_font("times", size=20, style='B')
            pdf.multi_cell(0, 10, subheader)
            pdf.set_font("times", size=12)
            pdf.multi_cell(0, 10, generated_text)

        pdf.output("output.pdf")
        st.session_state.report = ("\n").join(report)
    
    else :
        st.write(st.session_state.report)

# Streamlit app layout
def main():

    st.title(':card_index: Patient :blue[Insight]')

    if st.session_state.page == 0 :
        # User information form
        st.subheader("User Information / Analysis Options:")
        # Radio input for sex
        st.session_state.sex = st.radio("Select Sex:", ["Male", "Female"])

        # Numeric input for age
        st.session_state.age = st.number_input("Enter Age:", min_value=1, value=10, max_value=100)

        # Multi-select for Biochemistry
        st.session_state.biochemistry_options = st.multiselect("Select Biochemistry Analysis:", df[df["field"] == "BIOCHEMISTRY"]["mesure"])

        # Multi-select for Hematology
        st.session_state.hematology_options = st.multiselect("Select Hematology Analysis:", df[df["field"] == "HAEMATOLOGY"]["mesure"])

        if st.session_state.biochemistry_options or st.session_state.hematology_options : 
            st.button("Next", on_click=next)

    elif st.session_state.page == 1 :

        # User information form
        st.button("Back", on_click = back)

        st.subheader("Enter Analysis result:")

        if st.session_state.biochemistry_options :
            
            st.subheader(f"Biochemistry Analysis:")
            # Display form for selected Biochemistry options
        st.session_state.biochemistry_result = display_numeric_form(st.session_state.biochemistry_options, "BIOCHEMISTRY")

        # Display form for selected Hematology options
        if st.session_state.hematology_options :

            st.subheader(f"Hematology Analysis:")
            # Display form for selected Biochemistry options
        st.session_state.hematology_result = display_numeric_form(st.session_state.hematology_options, "HAEMATOLOGY")
 
        st.button("Generate Report", on_click=next)

    elif st.session_state.page == 2 :

        st.session_state.biochemistry_result.update(st.session_state.hematology_result)
        st.session_state.result = st.session_state.biochemistry_result

        generate_report()

        with open("output.pdf", "rb") as f:
            pdf_file = f.read()

        # Download button for the PDF
        st.download_button(label="Download report as PDF", data=pdf_file, file_name=f"lab_analysis_report.pdf")

        #Reset button
        st.button(label = "Reset", on_click=reset)


if __name__ == "__main__":
    main()