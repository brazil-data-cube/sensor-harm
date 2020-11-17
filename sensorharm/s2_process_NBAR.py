# Python Native
import sys
import time
# Sensorharm
from .sentinel2_harmonization import sentinel_harmonize, sentinel_harmonize_SAFE


if len(sys.argv) < 4:
    print('ERROR: usage: SAFEL1C, sr_dir, target_dir')
    sys.exit()


def main(safel1c, sr_dir, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)

    sentinel_harmonize(safel1c, sr_dir, target_dir)

    return


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    end = time.time()
    print(f'Duration time: {end - start}')
