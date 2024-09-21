import json
import yt_dlp
from transcriber import transcribe

URL = input()
transcribe(URL, False)
