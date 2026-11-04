import streamlit as st
import datetime
import os
from faster_whisper import WhisperModel
from moviepy import VideoFileClip
from translate import Translator

# Extract audio from video with MoviePy
def extract_audio(video_path, audio_path):
    # Load the video file
    video = VideoFileClip(video_path)
    # Extract the audio from the video
    audio = video.audio
    # Save the audio to the output path
    audio.write_audiofile(audio_path)
    # Close the audio file
    audio.close()
    # Close the video file
    video.close()

# Set up the Whisper model
model_size = "small.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
subpath = "files/"
os.makedirs(subpath, exist_ok=True)


# Transcribe an audio file
def transcribe_from_video(audio_path):
    segments, _ = model.transcribe(audio_path, )
    # Return the segments
    return segments

# Function to convert seconds to SRT timestamp format
def format_time(seconds):
    timestamp = str(datetime.timedelta(seconds=seconds))
    # Check if there is a fractional part in the seconds
    if '.' in timestamp:
        hours, minutes, seconds = timestamp.split(':')
        seconds, milliseconds = seconds.split('.')
        # Truncate the milliseconds to 3 decimal places
        milliseconds = milliseconds[:3]
    else:
        hours, minutes, seconds = timestamp.split(':')
        milliseconds = "000"
    # Return the formatted timestamp
    return f"{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)},{milliseconds.zfill(3)}"

# Function to generate SRT file from transcription data
def generate_srt(transcription_data, output_file, lang):
    # Open the output file
    with open(output_file, 'w', encoding="UTF-8") as srt_file:
        # Iterate over the transcription data
        for i, segment in enumerate(transcription_data):
            # Format the start and end times
            start_time = format_time(segment.start)
            end_time = format_time(segment.end)

            # Translate the text to the target language if it is not English
            if lang != "en":
                translator = Translator(from_lang="en", to_lang=lang)
                text = translator.translate(segment.text)
            else:
                text = segment.text

            # Write the segment data to the SRT file
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{text}\n\n")

# Set the page title in Streamlit
st.title("Video Captioning and Translating")

# Set the page description in Streamlit
st.write("Upload a video and get the captions and translations.")

# Select the language for translation
language = st.selectbox("Select the target language", ["en", "es", "fr", "de", "it", "pt"])

# Upload a video file
video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

# Check if the video file is uploaded and the language is selected
if video_file and language:
    # Display progress message
    with st.status("Processing the video...", expanded=True):
        # Save the video file temporarily
        st.write("Uploading the video...")
        with open(subpath + "output.mp4", "wb") as f:
            f.write(video_file.read())

        # Extract the audio from the video
        st.write("Extracting audio from the video...")
        extract_audio(subpath + "output.mp4", subpath + "output.wav")

        # Transcribe the audio file
        st.write("Transcribing the audio...")
        text_segments = transcribe_from_video(subpath + "output.wav")

        # Generate the SRT file
        st.write("Generating the SRT file...")
        generate_srt(text_segments, subpath + "output.srt", language)

    # Display the video file
    st.video(video_file, subtitles=subpath + "output.srt")
    
