import os
import shutil
import sys

PNG_MAGIC = b'\x89PNG\r\n\x1a\n'

def main() -> int:
    src = 'entry.png'
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', 'out')
    dst = os.path.join(out_dir, 'entry.png')

    if not os.path.exists(src):
        print(f'Source not found: {src}', file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copy2(src, dst)

    with open(dst, 'rb') as f:
        header = f.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        print('Copied file is not a valid PNG', file=sys.stderr)
        return 1

    size = os.path.getsize(dst)
    print(f'{dst} {size}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
