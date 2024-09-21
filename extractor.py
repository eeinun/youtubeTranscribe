import yt_dlp


def extract_audio(url):
    ydl_opts = {
        'format': 'mp4/b.3,m4a/bestaudio/best',
        'outtmpl': "tmp/%(id)s.%(ext)s",
        'overwrites': False,
        'paths': {
            'home': "C:\\Users\\mj008\\Documents\\youtubeTranscribe"
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        error_code = ydl.download([url])
    print(f"[extractor] Task complete with{(' error code' + error_code) if error_code else 'out any errors'}.")
    print(f"[extractor] Title: {info['title']}, language: {info['language']}")
    return info['title'], info['language']



if __name__ == "__main__":
    URLS = ['https://www.youtube.com/watch?v=h-PWth26dPo']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': "%(id)",
        'overwrites': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)