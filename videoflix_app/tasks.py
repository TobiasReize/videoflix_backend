import subprocess
from os.path import splitext


def convert_480p(source):
    base, ext = splitext(source)
    new_file = base + '_480p' + ext
    cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    result = subprocess.run(cmd, shell=True, capture_output=True)
    print("Returncode:", result.returncode)
    print("stdout:", result.stdout.decode())
    print("stderr:", result.stderr.decode())
