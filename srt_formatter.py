def hms(sec, ms_delim=','):
    msec = int(sec * 1000)
    sec = msec // 1000
    min = sec // 60
    hour = min // 60
    return f"{str(hour).zfill(2)}:{str(min % 60).zfill(2)}:{str(sec % 60).zfill(2)}{ms_delim}{str(msec % 1000).zfill(3)}"


def process_vjson_segment(segment, index_offset=0, time_offset=0):
    return f'''{segment['id'] + index_offset}
{hms(segment['start'] + time_offset)} --> {hms(segment['end'] + time_offset)}
{segment['text'].strip()}\n
'''