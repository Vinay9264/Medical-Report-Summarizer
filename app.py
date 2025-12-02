import streamlit as st
import requests
import base64
import os


API_URL = "http://127.0.0.1:8000/api/process"

st.set_page_config(page_title="Medical Report Summarizer", layout="wide")

def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("frontend/vector-may-2021-55.jpg")





#st.title("Medical Report Summarizer")
st.markdown(
    """
    <div style="display: flex; justify-content: flex-start; padding-left: 350px;">
        <h1>Medical Report summarizer</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("                                               ")
st.write(".")

st.markdown(
    "<p style='color: white; font-size: 22px;'>Upload any medical report (Image or PDF) and get a clean summary</p>",
    unsafe_allow_html=True
)




uploaded_file = st.file_uploader("Upload Report (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

mode_label = st.selectbox("Choose Summary Type", ["For Doctor", "For Patient"])
mode = "doctor" if mode_label == "For Doctor" else "patient"

st.markdown("""
    <style>
    div.stButton > button {
        background-color: #0066ff;
        color: white;
        border-radius: 8px;
        height: 45px;
        width: 150px;
        border: 2px solid #0047b3;
    }
    div.stButton > button:hover {
        background-color: #0047b3;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


if st.button("Process Report"):
    if uploaded_file is None:
        st.error("Please upload a file first.")
    else:
        with st.spinner("Processing... Please wait."):

            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            data = {"mode": mode}

            response = requests.post(API_URL, files=files, data=data)

            if response.status_code == 200:
                result = response.json()

                st.success("Processing complete!")

                st.subheader("Extracted Text")
                st.text_area("", result["extracted_text"], height=200)

                st.subheader("Cleaned Text")
                st.text_area("", result["cleaned_text"], height=200)

                st.subheader("Summary")
                st.text_area("", result["summary"], height=200)

            else:
                st.error("Error: Could not process file.")
