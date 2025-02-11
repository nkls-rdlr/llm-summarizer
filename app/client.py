from io import BytesIO
from markdown import markdown
import streamlit as st
from summarizer import generate_summary
from xhtml2pdf import pisa


def _convert_markdown_to_pdf(summary: str) -> None:
    """
    Generates a HTML-formatted PDF file from the Markdown summary, and stores
    it in a temporary cache to make it available for download.
    """
    summary_html = markdown(summary)
    pdf_cache = BytesIO()

    pisa.CreatePDF(summary_html, dest=pdf_cache)
    pdf_cache.seek(0)

    return pdf_cache


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

st.sidebar.subheader("A simple Streamlit app to transcribe and summarize YouTube "
             "videos")

st.sidebar.text("How it works: After you enter the URL of the YouTube video "
                "you want to summarize, the app downloads its audio, "
                "transcribes it using OpenAI Whisper and summarizes it using "
                "Llama 3.1 (8B).")

url = st.sidebar.chat_input("Paste the URL of the YouTube video here")

if url is not None:
    with st.spinner("Summarizing...", show_time=True):
        summary = generate_summary(url)

    if summary:
        st.sidebar.success("Video summarized successfully.")

        st.markdown(
            f"""
            <div style="border:1px solid #ddd; padding:10px; border-radius:5px; background-color:#f9f9f9; color: black;">
            {summary}
            </div>
            """,
            unsafe_allow_html=True
        )
        summary_pdf = _convert_markdown_to_pdf(summary)
        st.download_button(
            label="Download as PDF",
            data=summary_pdf,
            file_name="summary.pdf",
            mime="application/pdf"
        )
