import subprocess  # sudo apt-get install ffmpeg


def oga_2_wav(src_filename):
    dest_filename = src_filename.split('.')[0] + '.wav'
    subprocess.run(['ffmpeg', '-loglevel', 'warning', '-i', src_filename, dest_filename])
    return dest_filename
