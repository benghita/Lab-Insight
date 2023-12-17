# Import necessary libraries
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

st.set_page_config(
   page_title="Lab Insight",
   page_icon="🔬",
   initial_sidebar_state="expanded",
)

if 'history' not in st.session_state:
    st.session_state['history'] = []

csv_file_path = "./data.csv"

def conversational_chat(query):
    
    result = st.session_state.chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    
    return result["answer"]

def display_measure_info(search_term):
    
    st.markdown(f"**- Is {search_term} a blood test mesure :**")
    query = f"is {search_term} a blood test mesure? if yes give me a definition"
    st.markdown(conversational_chat(query))
    
    st.markdown(f"**- Is {search_term} availbale in the app :**")
    query = f"is {search_term} availbale in the provided data ? \n if yes list the following info in JSON format :the field, the mesure name and the unit"
    st.markdown(conversational_chat(query))
    st.session_state['history'] = []

# Streamlit app layout
def home_page():

    st.title(':microscope: Lab :blue[Insight]')

    # Introduction about the app
    st.markdown("""
    Lab Insight is your comprehensive guide to understanding blood test results. 
    Whether you're a patient or a medical professional, explore detailed insights and information about various blood measures.
    """)

    # Search bar for blood measures
    st.markdown(""":arrow_down_small: you can search for blood test measures to see if they are available in the app;
                 if so, the app will show you more information about it.""")
    search_term = st.text_input("Search for a Blood Measure:")
   
    # Load the CSV file with field, subfield, measure, etc.
    if 'chain' not in st.session_state :
        loader = CSVLoader(file_path=csv_file_path, encoding="utf-8", csv_args={'delimiter': ';'})
        data = loader.load()
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(data, embeddings)
        st.session_state.chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo'),
                                                retriever=vectorstore.as_retriever())

    if st.button("Search"):
        display_measure_info(search_term)


if __name__ == "__main__":
    home_page()