import argparse
from transcriber import transcribe
from agent import Agent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some arguments.")

    parser.add_argument('url', type=str, help='유튜브 영상 주소를 입력합니다.')
    parser.add_argument('-t', '--translate', action='store_true', help='영상의 주 언어가 한국어가 아니면 한국어로 번역합니다.')

    args = parser.parse_args()
    transcribe(args.url, args.translate, Agent())
