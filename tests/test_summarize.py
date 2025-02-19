from app.summarizer import YouTubeSummarizer
import os
import pytest

summarizer = YouTubeSummarizer()


def test_error_if_transcript_is_empty_format():
    """
    This test asserts that the format_transcript() function throws a ValueError
    if it is passed an empty or non-existent transcript.
    """
    empty_transcript = ""

    with pytest.raises(ValueError):
        summarizer.format_transcript(empty_transcript)


def test_error_if_transcript_is_empty_summarize():
    """
    This test asserts that the summarize_transcript() function throws a
    ValueError if it is passed an empty or non-existent transcript.
    """
    empty_transcript = ""

    with pytest.raises(ValueError):
        summarizer.summarize_transcript(empty_transcript)


@pytest.mark.skipif(bool(os.getenv("GITHUB_ACTIONS")))
def test_formatted_transcript_is_not_empty():
    """
    This test asserts that the format_transcript() function returns a non-empty
    string object when passed a valid string object.
    """
    with open("tests/fixtures/sample_transcript.txt", "r") as file:
        transcript = file.read()

    formatted_transcript = summarizer.format_transcript(transcript)

    assert formatted_transcript
    assert isinstance(formatted_transcript, str)


@pytest.mark.skipif(bool(os.getenv("GITHUB_ACTIONS")))
def test_summary_is_not_empty():
    """
    This test asserts that the summarize_transcript() function returns a
    non-empty string object when passed a valid string object.
    """
    with open("tests/fixtures/sample_transcript.txt", "r") as file:
        transcript = file.read()

    summary = summarizer.summarize_transcript(transcript)

    assert summary
    assert isinstance(summary, str)
