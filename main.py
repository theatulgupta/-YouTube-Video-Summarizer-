import streamlit as st
from summarizer import summarize_video

if __name__ == "__main__":
    st.set_page_config(page_title="YouTube Video Summarizer", page_icon=":clapper:")

    st.title("YouTube Video Summarizer")
    youtube_url = st.text_input("Enter YouTube URL")
    summarize_video(youtube_url)
