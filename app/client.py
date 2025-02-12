import asyncio
from io import BytesIO
from markdown import markdown
import streamlit as st
from summarizer import (
    download_audio,
    download_subtitles,
    transcribe_audio,
    format_transcript,
    summarize_transcript,
)
from typing import Tuple
from xhtml2pdf import pisa


def convert_markdown_to_pdf(summary: str) -> None:
    """
    Generates a HTML-formatted PDF file from the Markdown summary, and stores
    it in a temporary cache to make it available for download.
    """
    summary_html = markdown(summary)
    pdf_cache = BytesIO()

    pisa.CreatePDF(summary_html, dest=pdf_cache)
    pdf_cache.seek(0)

    return pdf_cache


async def process_transcript(transcript: str) -> Tuple[str, str]:
    """
    Given a transcript, asynchronously handles summarization and formatting.
    Returns both a summary and a formatted transcript to be served to the user.
    """
    loop = asyncio.get_event_loop()
    summarize_task = loop.run_in_executor(
        None, summarize_transcript, transcript
    )
    format_transcript_task = loop.run_in_executor(
        None, format_transcript, transcript
    )

    summary, formatted_transcript = await asyncio.gather(
        summarize_task, format_transcript_task
    )
    return summary, formatted_transcript


st.title("LLM Summarizer")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
    max-width: 750px;
    }
    """,
    unsafe_allow_html=True,
)

st.sidebar.subheader(
    "A simple Streamlit app to transcribe and summarize YouTube videos"
)

st.sidebar.text(
    "How it works: After you enter the URL of the YouTube video you want to "
    "summarize, the app downloads its audio, transcribes it using OpenAI "
    "Whisper and summarizes it using Llama 3.1 (8B)."
)

url = st.sidebar.chat_input("Paste the URL of the YouTube video here")

transcript_option = st.sidebar.selectbox(
    "Which source should be used for the summary?",
    (
        "LLM-generated transcript", "Subtitles"
    )
)

if url:
    if transcript_option == "Subtitles":
        with st.spinner("Downloading subtitles", show_time=True):
            try:
                transcript = download_subtitles(url)
            except Exception as e:
                st.error(
                    "Subtitles could not be downloaded. Downloading "
                    "audio for transcription."
                )
                file_path = download_audio(url)
                transcript = transcribe_audio(file_path)
    else:
        with st.spinner("Downloading audio", show_time=True):
            file_path = download_audio(url)
        with st.spinner("Transcribing audio", show_time=True):
            transcript = transcribe_audio(file_path)

    if transcript:
        with st.spinner("Summarizing transcript", show_time=True):
            summary, formatted_transcript = asyncio.run(
                process_transcript(transcript)
            )

    if summary and formatted_transcript:
        st.sidebar.success("Video summarized successfully")

        st.markdown(
            f"""
            <div style="border:1px solid #ddd; padding:10px; border-radius:5px; background-color:#f9f9f9; color: black;">
            {summary}
            </div>
            """,
            unsafe_allow_html=True,
        )

        summary_pdf = convert_markdown_to_pdf(summary)
        transcript_pdf = convert_markdown_to_pdf(formatted_transcript)

        dl_summary, dl_transcript = st.columns(2)

        with dl_summary:
            st.download_button(
                label="Download Summary",
                data=summary_pdf,
                file_name="summary.pdf",
                mime="application/pdf",
            )

        with dl_transcript:
            st.download_button(
                label="Download Transcript",
                data=transcript_pdf,
                file_name="transcript.pdf",
                mime="application/pdf",
            )
