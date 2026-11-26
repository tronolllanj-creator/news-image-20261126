import os
import shutil
import sys

def main() -> int:
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', 'out')
    os.makedirs(output_dir, exist_ok=True)
    
    src = 'entry.png'
    dst = os.path.join(output_dir, 'entry.png')
    
    shutil.copy2(src, dst)
    
    with open(dst, 'rb') as f:
        magic = f.read(8)
    
    if magic != b'\x89PNG\r\n\x1a\n':
        print(f'ERROR: {dst} does not start with PNG magic bytes', file=sys.stderr)
        return 1
    
    size = os.path.getsize(dst)
    print(f'{dst} {size}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
