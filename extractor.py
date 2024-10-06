import math
import re

import yt_dlp
import subprocess
from os.path import getsize

from srt_formatter import hms


def extract_youtube(url, seg_size, maximum_size):
    ydl_opts = {
        'format': 'mp4/b.3,m4a/bestaudio/best',
        'outtmpl': "tmp/%(title)s.%(ext)s",
        'overwrites': False,
        'paths': {
            'home': "C:\\Users\\mj008\\Documents\\youtubeTranscribe"
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        error_code = ydl.download([url])
    print(f"[extractor] Task complete with{(' error code' + error_code) if error_code else 'out any errors'}.")
    return size_handler(info['title'], seg_size, maximum_size), info['language']


def size_handler(name, seg_size, maximum_size):
    print(f'[extractor] Checking file size "tmp/{name}.m4a"')
    probe_result = subprocess.run(
        f'ffmpeg.exe -i "tmp/{name}.m4a" 2>&1',
        shell=True,
        capture_output=True
    ).stdout.decode("utf-8")
    h, m, s, s_ = map(int, re.split(r"[\.:]", (re.findall(r"Duration: (\d+:\d+:\d+\.\d*),", probe_result))[0]))
    duration = h * 3600 + m * 60 + s + s_ / 1000
    if getsize(f"tmp/{name}.m4a") > maximum_size:
        print(f"[extractor] File size exceeds maximum duration. "
              f"Split it into {hms(int(seg_size), ms_delim='.')} size segments. "
              f"This can cause some loss near boundary.")
        segmentation(f"tmp/{name}.m4a", segment_time=seg_size)
        n = math.ceil(duration / seg_size)
        return [(f"tmp/{name}_{x:03}.m4a", (x * seg_size, (x + 1) * seg_size), x) for x in range(n)]
    return [(f"tmp/{name}.m4a", (0, duration), 0)]


def extract_local(path, output_name, seg_size, maximum_size):
    print("[extractor] Extract audio from local file", path)
    subprocess.run(
        f'ffmpeg.exe -hide_banner -v warning -stats -i "{path}" -q:a 0 -map a -b:a 92k "tmp/{output_name}.m4a"',
        input=b"n\n"
    )
    return size_handler(output_name, seg_size, maximum_size), None


def segmentation(path, segment_time=1800):
    subprocess.run(
        f'ffmpeg.exe -hide_banner -v warning -stats -i "{path}" -f segment -segment_time {segment_time} -b:a 92k "{path.split(".")[0]}_%03d.m4a"'
    )