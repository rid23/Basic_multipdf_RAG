import streamlit as st
import os

st.set_page_config(page_title="RAG UI", page_icon=":books:", layout="wide")

UPLOAD_DIR = "pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("📂 Drag & Drop File Upload")
st.write("Drag and drop your files below to upload them. You can also click the area to select files from your computer.")
uploaded_files = st.file_uploader("Upload your files here", accept_multiple_files=True , 
    type=["pdf", "docx", "txt"]
                    )
st.markdown("""
    <style>
        .stFileUploader {
            border: 2px dashed #4CAF50;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)
if uploaded_files:
    st.write("Uploaded Files:")
    for uploaded_file in uploaded_files:
        st.write(f"- {uploaded_file.name} ({uploaded_file.size} bytes)")

    #save the uploaded files to the /pdfs directory
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Files uploaded successfully!")
    