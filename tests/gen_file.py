# -*- encoding: utf-8 -*-

from pathlib import Path
from itertools import cycle


def concat_files(path, glob='*.txt', out='out.txt'):
    directory = Path(path)
    content_files = directory.glob(glob)
    with Path(out).open('wb') as f:
        size = 0
        limit = 40 * 10 ** 6  # 10**6 = MB
        for content in cycle(content_files):
            data = content.read_bytes()
            f.write(data)
            if size > limit:
                break
            size += len(data)

if __name__ == '__main__':
    concat_files('./txts')