import subprocess
from os.path import splitext
import getpass


def convert_120p(source):
    print("Worker läuft als:", getpass.getuser())
    base, ext = splitext(source)
    new_file = base + '_120p' + ext
    # cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s 214x120 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    cmd = 'ffmpeg -i "{}" -s 214x120 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("Returncode_120p:", result.returncode)
    print("stdout_120p:", result.stdout)
    print("stderr_120p:", result.stderr)


def convert_360p(source):
    base, ext = splitext(source)
    new_file = base + '_360p' + ext
    # cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s 640x360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    cmd = 'ffmpeg -i "{}" -s 640x360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("Returncode_360p:", result.returncode)
    print("stdout_360p:", result.stdout)
    print("stderr_360p:", result.stderr)


def convert_720p(source):
    base, ext = splitext(source)
    new_file = base + '_720p' + ext
    # cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("Returncode_720p:", result.returncode)
    print("stdout_720p:", result.stdout)
    print("stderr_720p:", result.stderr)


def convert_1080p(source):
    base, ext = splitext(source)
    new_file = base + '_1080p' + ext
    # cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("Returncode_1080p:", result.returncode)
    print("stdout_1080p:", result.stdout)
    print("stderr_1080p:", result.stderr)
