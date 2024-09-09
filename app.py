import streamlit as st
import face_recognition as fr
import os
from PIL import Image

import os

if not os.path.exists('temp'):
    os.makedirs('temp')

# Function to load an image and get its encoding
def get_encoding(image_path):
    image = fr.load_image_file(image_path)
    encoding = fr.face_encodings(image)
    if encoding:  # Check if any faces were detected
        return encoding[0]  # Return the first face encoding
    else:
        return None

# Streamlit app

st.markdown('''
    <h1 style='text-align: center; display: inline;'>Face Recognition App </h1>
    <span style='text-align: center; display: inline; font-size: 20px;'>by Saurabh </span>
''', unsafe_allow_html=True)

# Upload images
uploaded_images = st.file_uploader("Upload three images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_images:
    # Load and process the uploaded images
    image_encodings = []
    for uploaded_image in uploaded_images:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        image_path = os.path.join("temp", uploaded_image.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        encoding = get_encoding(image_path)
        if encoding is not None:
            image_encodings.append(encoding)
        else:
            st.warning(f"No face detected in {uploaded_image.name}")

    # Compare faces and display results
    if len(image_encodings) >= 2:
        for i in range(len(image_encodings) - 1):
            for j in range(i + 1, len(image_encodings)):
                face_distances = fr.face_distance([image_encodings[i]], image_encodings[j])
                match = face_distances[0] < 0.6  # Adjust the threshold as needed

                st.write(f"**Comparing Image {i+1} and Image {j+1}**")
                st.write(f"Distance: {face_distances[0]:.2f}")
                st.write(f"Match: {match}")
    else:
        st.warning("Please upload at least two images with detectable faces for comparison.")