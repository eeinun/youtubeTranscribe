import argparse
import re
from os.path import isfile
from agent import Agent
from extractor import *
from transcriber import *
from translator import *
from srt_formatter import process_vjson_segment


def common_procedure(audio_segments, lang):
    seg_index = 0
    path_splitter = r'([/\\]|\\\\)'
    if len(audio_segments) == 1:
        srt_name = f"tmp/{'.'.join(re.split(path_splitter, audio_segments[0][0])[-1].split('.')[:-1])}.srt"
    else:
        srt_name = f"tmp/{'_'.join(re.split(path_splitter, audio_segments[0][0])[-1].split('_')[:-1])}.srt"
    if isfile(srt_name):
        with open(srt_name, "w") as f:
            f.write("\r")
    for i in audio_segments:
        segments, lang = transcribe(i[0], agent, lang)
        if lang not in agent.iso639.keys():
            try:
                lang = agent.iso639[lang]
            except KeyError:
                lang = None
        else:
            lang = None
        if args.translate:
            translate_segments(segments, agent)
        with open(srt_name, "a", encoding="utf-8") as f:
            print(f"[transcriber] Writing subtitle file. {srt_name}")
            for seg in segments:
                f.write(process_vjson_segment(seg, index_offset=seg_index, time_offset=(seg_length * i[-1])))
        seg_index += len(segments)


if __name__ == "__main__":
    agent = Agent()
    seg_length, maximum_size = 1800, 25000000
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', action='store_true', help='개인데이터를 수정합니다.')
    parser.add_argument('-u', '--url', type=str, help='유튜브 영상의 주소를 입력합니다.', nargs='*', default=[])
    parser.add_argument('-p', '--path', type=str, help='로컬에 저장된 영상의 경로를 입력합니다.', nargs='*', default=[])
    parser.add_argument('-t', '--translate', action='store_true', help=f'영상의 주 언어가 설정된 언어({agent.lang})가 아니면 번역합니다.')

    args = parser.parse_args()

    if args.config:
        agent.modify()
        exit()

    for i in args.url:
        if re.match(r"(https://)?(www.youtube.com/watch.+|youtu.be/.+)", i) is None:
            print(f"[main] Invalid url: {i}")
        else:
            print(f"[main] Transcribing youtube video {i}...")
            common_procedure(*extract_youtube(i, seg_length, maximum_size))
            print()

    for i in args.path:
        if not isfile(i):
            print(f"Invalid path: {i}")
        else:
            print(f"[main] Transcribing local video {i}...")
            name = re.split(r"([\\/]|\\\\)", i)[-1].split('.')[0]
            common_procedure(*extract_local(i, name, seg_length, maximum_size))
            print()

    print("All tasks completed.")

