import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig
import os
from dotenv import load_dotenv

load_dotenv()


proxy_username = os.getenv("WEBSHARE_PROXY_USERNAME")
proxy_password = os.getenv("WEBSHARE_PROXY_PASSWORD")

def extract_video_id(youtube_url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.

    Example:
    https://www.youtube.com/watch?v=IHZwWFHWa-w
    -> IHZwWFHWa-w
    """

    match = re.search(r"v=([^&]+)", youtube_url)

    if not match:
        raise ValueError("Invalid YouTube URL")

    return match.group(1)


def fetch_transcript(video_id: str) -> str:
    """
    Fetches the English transcript and returns it as a single string.
    """

    try:
        ytt_api = YouTubeTranscriptApi(
            proxy_config = WebshareProxyConfig(
                proxy_username=proxy_username, 
                proxy_password=proxy_password,
                # filter_ip_locations=['india']
            )
        )
        transcript_data = ytt_api.fetch(
            video_id=video_id,
            languages=["en"]
        )

        transcript = " ".join(
            snippet.text for snippet in transcript_data
        )

        return transcript

    except TranscriptsDisabled:
        raise Exception(
            "Transcripts are disabled for this video."
        )

    except NoTranscriptFound:
        raise Exception(
            "No English transcript found for this video."
        )

    except Exception as e:
        raise Exception(
            f"Failed to fetch transcript: {str(e)}"
        )


def get_transcript_from_url(youtube_url: str) -> str:
    """
    Complete pipeline:
    URL -> Video ID -> Transcript
    """

    video_id = extract_video_id(youtube_url)

    transcript = fetch_transcript(video_id)

    return transcript