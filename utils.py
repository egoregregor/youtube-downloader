import re
import os


def format_duration(duration):
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours, minutes, seconds = [int(part[:-1]) if part else 0 for part in match.groups()]
    if hours:
        return f'{hours}:{minutes:02d}:{seconds:02d}'
    elif minutes:
        return f'{minutes}:{seconds:02d}'
    else:
        return f'0:{seconds:02d}'


def format_filesize_mb(filesize_bytes):
    filesize_mb = filesize_bytes / (1024 * 1024)
    formatted_size = "{:.1f} MB".format(filesize_mb)
    return formatted_size


def current_directory():
    return os.getcwd()
