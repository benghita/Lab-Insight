# Import necessary libraries
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.prompts import SystemMessagePromptTemplate
import pandas as pd
from fpdf import FPDF

# page configuration
st.set_page_config(
   page_title="Lab Insight",
   page_icon="🔬",
   initial_sidebar_state="expanded",
)

# Initialization of session_state variabals and functions
if "patient_page" not in st.session_state : 
    st.session_state.patient_page = 0

if 'history' not in st.session_state:
    st.session_state['history'] = []

if "pateint_report" not in st.session_state :
    st.session_state.pateint_report = []

def next():
    st.session_state.patient_page = st.session_state.patient_page + 1

def back():
    st.session_state.patient_page = st.session_state.patient_page - 1

def reset():
    st.session_state.patient_page = 0
    st.session_state.pateint_report = []

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

def conversational_chat(query):
    
    result = st.session_state.chain({"question": query, 
    "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    
    return result["answer"]

# Initialize a FPDF object
def create_pdf():
    title = "Lab insight Report"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 15)
    pdf.set_auto_page_break(auto=True)
    # Calculate width of title and position
    w = pdf.get_string_width(title) + 6
    pdf.set_x((210 - w) / 2)
    # Colors of frame, background and text
    pdf.set_draw_color(53, 89, 224)
    pdf.set_fill_color(255, 236, 214)
    pdf.set_text_color(15, 33, 103)
    # Thickness of frame (1 mm)
    pdf.set_line_width(1)
    # Title
    pdf.cell(w, 9, title, 1, 1, 'C', 1)
    # Line break
    pdf.ln(10)
    return pdf

def add_to_pdf(pdf, subheader, text):
    # Arial 12
    pdf.set_font('Arial', '', 12)
    # Background color
    pdf.set_fill_color(200, 220, 255)
    # Title
    pdf.cell(0, 6, subheader, 0, 1, 'L', 1)
    # Line break
    pdf.ln(4)
    # Times 12
    pdf.set_font('Times', '', 12)
    # Output justified text
    pdf.multi_cell(0, 5, text)
    # Line break
    pdf.ln()

def get_answer(query, chain):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    generated_text = result["answer"]
    st.session_state['history'].append((query, generated_text))
    return generated_text

def save_and_print(report, subheader, generated_text, pdf):
    
    # Save report
    report.append(subheader)
    report.append(generated_text)

    # Print results
    st.write(f"**{subheader}**")
    st.markdown(generated_text)
    
    # Save in fpdf object
    add_to_pdf(pdf, subheader, generated_text)

    return report

# Function to generate and save a report using GPT-3.5-turbo
def generate_report():

    # Define embedding
    embedding = OpenAIEmbeddings()

    pdf = create_pdf()

    st.subheader("Generated Report", divider = "blue")

    if not st.session_state.pateint_report:
        
        report = []
        # Define the system message template
        system_template ="""You are a helpful medical professional
                        and you will receive a patient's blood test results.
                        Your job is to explain the meaning of the result in general and to answer the patient's questions without asking any farther info.
                        Keep in mind that the patient may not understand basic medical concepts.
                        make sure to write directly a detailed and general answer.
                        ----------------
                        {context}"""
        # Create the chat prompt templates
        messages = [SystemMessagePromptTemplate.from_template(system_template),
                    HumanMessagePromptTemplate.from_template("{question}")]
        qa_prompt = ChatPromptTemplate.from_messages(messages)
        user_info = f"considering that : sex = {st.session_state.sex}, age = {st.session_state.age}"
        for mesure in st.session_state.result.keys() : 
            
            section = df[df["mesure"] == mesure]["section"]
            field = df[df["mesure"] == mesure]["field"]

            # Define and run prompt
            query = f"""waht is the meaning of {st.session_state.result[mesure]}? {user_info}"""
            user_info = ""
            
            vectordb = Chroma(embedding_function = embedding,
                              persist_directory = f"{persist_dir}{field}/{section}")

            chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature = 0.0, model_name = 'gpt-3.5-turbo'),
                                                combine_docs_chain_kwargs={"prompt": qa_prompt} ,
                                                retriever = vectordb.as_retriever())
            generated_text = get_answer(query, chain)

            subheader = f"- {mesure} :"
            # Save report
            report = save_and_print(report, subheader, generated_text, pdf)

        query = f"""waht are Possible causes of abnormal results?"""
        generated_text = get_answer(query, chain)
        subheader = "-  Possible causes of abnormal results :"
        report = save_and_print(report, subheader, generated_text, pdf)
        
        query = f"""is there any Recommendations of What I should do next?"""
        generated_text = get_answer(query, chain)
        subheader = "-  Recommendations :"
        report = save_and_print(report, subheader, generated_text, pdf)

        pdf.output("output.pdf")
        st.session_state.pateint_report = report
    
    else :
        for i in st.session_state.pateint_report: 
            st.write(i)

# Streamlit app layout
def main():

    st.title(':card_index: Patient :blue[Insight]')

    if st.session_state.patient_page == 0 :
        # User information form
        st.subheader("Patient Information / Analysis Options:")
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

    elif st.session_state.patient_page == 1 :

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

    elif st.session_state.patient_page == 2 :

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