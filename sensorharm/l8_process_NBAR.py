# Python Native
import sys
import time
# Sensorharm
from .landsat_harmonization import landsat_harmonize


if len(sys.argv) < 3:
    print('ERROR: usage: satsen, productdir, target_dir')
    sys.exit()


def main(satsen, productdir, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)

    landsat_harmonize(satsen, productdir, target_dir)

    return


if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    end = time.time()
    print("Duration time: {}".format(end - start))
