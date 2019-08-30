#!/usr/bin/python3

from os import path, remove
from tempfile import gettempdir
from random import random
import subprocess
import argparse
import re

DESC = """
Скрипт для создания gif из видео с помощью ffmpeg.

Использует генерацию палитры в режиме stats_mode=full,
с дизерингом sierra2_4a.

Умеет менять высоту и частоту кадров выходному файлу.

Примеры:
    gif.py input.mkv output.gif - перекодирует в gif,
    частоту кадров поставит не больше 30

    gif.py input.mkv -r 15 output.gif - поставит fps уже на 15

    gif.py input.mkv -r 15 -v 300 output.gif - fps на 15 и высота на 300px
"""
EPI = """
Источники вдохновения
    http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
    https://github.com/lukechilds/gifgen
"""
def get_args():
    parser = argparse.ArgumentParser(
        description = DESC,
        formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position = 40),
        epilog = EPI
    )
    requiredNamed = parser.add_argument_group("required arguments")
    requiredNamed.add_argument('infile', help = 'Путь к исходному видео')
    parser.add_argument('--fps', '-r', help = 'Желаемый fps gif', type = float or int, default = None)
    parser.add_argument('--height', '-v', help = 'Высота gif', type = int, default = None)
    requiredNamed.add_argument('outfile', help = 'Путь к gif')
    return parser.parse_args()

def get_fps(fp):
    p = subprocess.Popen(
        ['ffmpeg', '-i', fp],
        stderr = subprocess.PIPE
    )
    out, err = p.communicate()
    return float(
        re.search(
            '(\d+(\.\d+)?) fps',
            err.decode('utf-8')
        ).group()[:-4]
    )

def _get_scale_str(height):
    return 'scale=-2:{}:flags=lanczos,'.format(height) if height else ''

def gen_pal(fp, fpal, fps, height):
    p = subprocess.Popen([
        'ffmpeg',
        '-v', 'warning',
        '-i', fp,
        '-vf', 'fps={},{}palettegen=stats_mode=full'.format(
            fps,
            _get_scale_str(height)
        ),
        '-y', fpal
    ])
    p.communicate()

def encode(fp, out, pal, fps, height):
    p = subprocess.Popen([
        'ffmpeg',
        '-v', 'warning',
        '-i', fp,
        '-i', pal,
        '-lavfi', 'fps={},{}paletteuse=dither=sierra2_4a:diff_mode=rectangle'.format(
            fps,
            _get_scale_str(height)
        ),
        out
    ])
    p.communicate()

if __name__ == "__main__":

    args = get_args()

    temp_pal = path.join(gettempdir(), str(random()) + '.png')

    if args.fps is None:
        args.fps = get_fps(args.infile)
        if args.fps > 30:
            args.fps = 30

    gen_pal(args.infile, temp_pal, args.fps, args.height)
    encode(args.infile, args.outfile, temp_pal, args.fps, args.height)

    try:
        remove(temp_pal)
    except:
        pass
