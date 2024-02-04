import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

# Function to extract YouTube video ID from URL
def extract_video_id(url):
    try:
        video_id = None
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be" in url:
            video_id = url.split("/")[-1]
        return video_id
    except IndexError as e:
        print(f"Video ID not found in the URL: {e}")
        return None


# Function to extract transcript details from YouTube video ID
def extract_transcript_details(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join(item["text"] for item in transcript_list)
        return transcript
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to generate Gemini content from transcript text and prompt
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to summarize video
def summarize_video(youtube_url):
    video_id = extract_video_id(youtube_url)

    if video_id:
        # Display a loading spinner while fetching the thumbnail
        with st.spinner("Fetching thumbnail..."):
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
            thumbnail = st.image(thumbnail_url, use_column_width=True)
        # Replace the spinner with the actual image
        thumbnail.image(thumbnail_url, use_column_width=True)
    else:
        st.write("Invalid YouTube URL.")

    if st.button("Generate Summary"):
        transcript_text = extract_transcript_details(video_id)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown('## Detailed Summary:')
            st.write(summary)
        else:
            st.write("Transcript not found for the given YouTube video.")
