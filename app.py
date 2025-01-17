import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key="AIzaSyBjEeTXoxrkk3eFc_o_CAfHMIfgWglPrlU")

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary
within 200 words. Please provide the summary of the text given here:  """
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Video Summarizer")
video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    try:
        # Extract video ID from the URL
        if "youtube.com" in video_url:
            video_id = video_url.split("v=")[-1]
        elif "youtu.be" in video_url:
            video_id = video_url.split("/")[-1]
        else:
            st.error("Invalid YouTube URL!")
            video_id = None

        if video_id:
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
            # Fetch subtitles
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            data = ""
            for transcript in transcript_list:
                if transcript.is_translatable:
                    subtitles = transcript.translate('en').fetch()
                    data += " ".join([entry['text'] for entry in subtitles])
                    break

            # Display subtitles
            if data:
                st.subheader("Extracted Subtitles")
                st.write(data)

                # Summarize subtitles
                if st.button("Summarize"):
                    with st.spinner("Summarizing..."):
                        summary = generate_gemini_content(data, prompt)
                        st.subheader("Summary")
                        st.write(summary)
            else:
                st.warning("No subtitles found for this video.")

    except Exception as e:
        st.error(f"An error occurred: {e}")