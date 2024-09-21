import json


def hms(sec, ms_delim=','):
    msec = int(sec * 1000)
    sec = msec // 1000
    min = sec // 60
    hour = min // 60
    return f"{str(hour).zfill(2)}:{str(min % 60).zfill(2)}:{str(sec % 60).zfill(2)}{ms_delim}{str(msec % 1000).zfill(3)}"


def process_vjson_segment(segment):
    return f'''{segment['id']}
{hms(segment['start'])} --> {hms(segment['end'])}
{segment['text'].strip()}\n
'''