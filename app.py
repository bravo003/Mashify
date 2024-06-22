import os
import shutil
import streamlit as st
from main import main_script

# Constants
VIDEO = 'Video Song Files'
OUTPUT = 'mashup.mp3'
ZIP = 'mashup.zip'

# Streamlit app
st.title("Mashify")
st.write("""
    Welcome to Mashify! 
    This tool allows you to create a mashup of your favorite singer's video songs.
    Just enter the required details below and let us handle the rest.
""")

singer = st.text_input("Enter the singer's name:", placeholder="e.g., Adele")
count = st.number_input("Number of videos to download:", min_value=1, max_value=20, value=5, help="Select the number of video songs to include in the mashup.")
duration = st.number_input("Duration of each audio clip (seconds):", min_value=1, max_value=60, value=30, help="Specify the length of each audio clip in the mashup.")
email = st.text_input("Enter your email address:", placeholder="e.g., youremail@example.com")

# Create Mashup button
if st.button("Create Mashup"):
    if not singer:
        st.error("Please provide the singer's name.")
    elif not email:
        st.error("Please provide your email address.")
    else:
        # Ensure the video folder exists
        if not os.path.exists(VIDEO):
            os.makedirs(VIDEO)
        
        # Run the script
        with st.spinner("Creating mashup, please wait..."):
            main_script(singer, count, duration, email)
        
        st.success("Mashup created and sent successfully! Check your email for the download link.")

        # Clean up video files after process
        if os.path.exists(VIDEO):
            shutil.rmtree(VIDEO)

        if os.path.exists(OUTPUT):
            os.remove(OUTPUT)
        
        if os.path.exists(ZIP):
            os.remove(ZIP)

# Additional information
st.write("""
    **Note:** The process might take a few minutes depending on the number of videos and the duration of clips selected.
    Please ensure the email address provided is correct to receive the mashup file.
""")
