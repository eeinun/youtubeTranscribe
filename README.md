## Dependency
- Windows 11 에서 작성되고 테스트되었음
- 같은 디렉토리에 [`ffmpeg.exe`](https://ffmpeg.org/download.html)가 있어야 함
- 라이브러리 의존성 ([requirement.txt](https://github.com/eeinun/youtubeTranscribe/blob/master/requirements.txt) 참조)
  - `yt-dlp`
  - `openai` : api key 필요함.
  - `deepl` : api key 필요함.
## `main.py`
### Usage
```
python main.py [-h] [-c] [-u [URL ...]] [-p [PATH ...]] [-t]
```
### Options
- `-h`, `--help`: show this help message and exit
- `-c`, `--config`: 개인데이터를 수정합니다. `agent.py` 문단 참조.
- `-u [URL ...]`, `--url [URL ...]`: 유튜브 영상의 주소를 입력합니다.
- `-p [PATH ...]`, `--path [PATH ...]`: 로컬에 저장된 영상의 경로를 입력합니다.
- `-t, --translate`: 영상의 주 언어가 설정된 언어가 아니면 번역합니다.
## `agent.py`
개인화 정보 관리용
### Usage
```
python agent.py
```
### Options
1. OpenAI api secret
    - openai api key 수정
2. DeepL api secret
    - deepl api key 수정
3. Language
    - 번역 타깃 언어 설정
4. Finish
    - 종료