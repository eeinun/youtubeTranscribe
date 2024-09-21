from openai import OpenAI
from extractor import extract_audio
from srt_formatter import process_vjson_segment
from translator import translate_deepl
import re
import json
from os.path import isfile


def transcribe(url, agent, trans=True):
    client = OpenAI(api_key=agent.openai)
    vid = re.search("https://www.youtube.com/watch\?v=([_A-Za-z0-9\-]+)&?.*", url)
    if not vid:
        print("Invalid URL")
        exit()
    vid = vid.group(1)
    title, lang = extract_audio(url)
    if isfile(f"./tmp/{vid}.srt"):
        print(f"""[transcriber] Subtitle file "./tmp/{vid.group(1)}.srt" already exists.""")
        return

    audio_file = open(f"./tmp/{vid}.m4a", "rb")
    print("[transcriber] API call engaged.")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        language=lang
    )
    print("[transcriber] Got API response.")
    segments = transcript.segments
    if lang != "ko" and trans:
        print("[transcriber] Translating subtitle.")
        batch = []
        for i in segments:
            batch.append(i['text'])
        translation = translate_deepl(batch, agent.deepl)
        for i in range(len(segments)):
            segments[i]['text'] = translation[i]

    with open(f"./tmp/{vid}.srt", "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(process_vjson_segment(seg))

    print(f"[transcriber] Task complete. The video id was {vid}")


