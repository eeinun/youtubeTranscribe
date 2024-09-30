from openai import OpenAI
from openai._types import NOT_GIVEN
from extractor import extract_youtube, extract_local
from srt_formatter import process_vjson_segment
from translator import translate_deepl
from agent import Agent
import re
import json
from os.path import isfile


def transcribe(path, agent, video_language=None, vtt_format=False):
    client = OpenAI(api_key=agent.openai)
    audio_file = open(path, "rb")
    print("[transcriber] API call engaged.")
    if video_language is None:
        video_language = NOT_GIVEN
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        language=video_language
    )
    print("[transcriber] Got API response.")
    segments = transcript.segments
    return segments, transcript.language
