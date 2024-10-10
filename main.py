import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import os
import requests
from io import BytesIO

def get_audio_content_from_url(audio_url):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.RequestException as err:
        st.error(f"Error fetching audio content: {err}")
        return None

def audio_dubbing(user_choice, audio_source):
    st.write("Executing audio dubbing...")

    # Check if the audio source is a URL
    if audio_source.startswith(('http://', 'https://')):
        audio_content = get_audio_content_from_url(audio_source)
        if audio_content is None:
            st.error("Error fetching audio from URL.")
            return
    else:
        # Save the uploaded audio file to a temporary file
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_source.read())

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Recognize speech from the audio file
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        audio_text = recognizer.recognize_google(audio_data)

    # Print the recognized text
    st.write("Recognized Text:")
    st.write(audio_text)

    # Translate the recognized English text to the target language
    translator = Translator()
    translated_text = translator.translate(audio_text, src='en', dest=user_choice).text

    # Create a Text-to-Speech object for the translated text
    tts = gTTS(text=translated_text, lang=user_choice)

    # Save the TTS audio to a temporary file
    output_audio_path = f'output_audio_{user_choice}.mp3'
    tts.save(output_audio_path)

    # Display the output audio
    st.audio(output_audio_path, format="audio/mp3")

    # Clean up temporary files
    if not audio_source.startswith(('http://', 'https://')):
        os.remove(temp_audio_path)
    os.remove(output_audio_path)

    st.success("Audio dubbing complete!")
    st.balloons()

def main():
    st.title("ANUVADAK - Audio Dubbing")

    # Option to upload audio file or provide URL
    upload_option = st.radio("Choose audio source:", ("Upload Audio", "Enter Audio URL"))
    if upload_option == "Upload Audio":
        audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
    else:
        audio_file = None

    if audio_file is not None or upload_option == "Enter Audio URL":
        if upload_option == "Upload Audio":
            st.audio(audio_file, format="audio/wav")
        else:
            audio_url = st.text_input("Enter Audio URL")
            if audio_url:
                st.audio(audio_url, format="audio/wav")

        # Language selection for dubbing
        target_language = st.selectbox("Select Target Language", ['hi', 'ta', 'ma', 'bn', 'gu', 'kn', 'ur'])

        if st.button("Dub Audio"):
            # Dub the audio
            audio_dubbing(target_language, audio_file if audio_file else audio_url)

if __name__ == "__main__":
    main()

footer = """<style>
.footer {
    position:fixed;
    left:0;
    bottom:0;
    width:100%;
    background-color:black;
    color:white;
    text-align:center;
}
</style>
<div class="footer">
    <p>Developed by DIGITAL_DYNAMOSS</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
