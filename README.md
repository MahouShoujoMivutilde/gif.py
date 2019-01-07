# gif.py

Как правило, дает лучшее качество в ущерб размеру.

```
usage: gif.py [-h] [--fps FPS] [--height HEIGHT] infile outfile

Скрипт для создания gif из видео с помощью ffmpeg.

Использует генерацию палитры в режиме stats_mode=full,
с дизерингом sierra2_4a.

Умеет менять высоту и частоту кадров выходному файлу.

Для определения fps исходника использует ffprobe.

Примеры:
    gif.py input.mkv output.gif - перекодирует в gif,
    частоту кадров поставит не больше 30

    gif.py input.mkv -r 15 output.gif - поставит fps уже на 15

    gif.py input.mkv -r 15 -v 300 output.gif - fps на 15 и высота на 300px

optional arguments:
  -h, --help                  show this help message and exit
  --fps FPS, -r FPS           Желаемый fps gif
  --height HEIGHT, -v HEIGHT  Высота gif

required arguments:
  infile                      Путь к исходному видео
  outfile                     Путь к gif

Источники вдохновения
    http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
    https://github.com/lukechilds/gifgen
```