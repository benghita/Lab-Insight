# Import necessary libraries
import streamlit as st
import pandas as pd

st.set_page_config(
   page_title="Lab Insight",
   page_icon="🔬",
   initial_sidebar_state="expanded",
)

# Load data from CSV file
csv_file_path = "./data.csv"
data_df = pd.read_csv(csv_file_path, delimiter=";")

# PDF guide link
pdf_guide_url = "https://www.ampath.co.za/pdfs/Desk-Reference-web.pdf"

# Streamlit app layout
def main():
    st.title(":information_source: Source :blue[Details]")

    # Data Overview section
    st.subheader("Measures Overview:")
    st.dataframe(data_df) 

    # Privacy and Security section
    st.subheader("Privacy and Security:")
    st.markdown("Once you close the app, all your data will be automatically deleted. We do not save any user data.")

    # References section
    st.subheader("References:")
    st.markdown(f"Check the [Guide to Laboratory Tests]({pdf_guide_url}) for more information.")

# Run the Streamlit app
if __name__ == "__main__":
    main()