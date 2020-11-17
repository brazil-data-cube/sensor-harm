# Python Native
import time
# 3rdparty
import sensor_harm


start = time.time()

sr_dir = '/path/to/L8/SR/images/'
target_dir = '/path/to/output/NBAR/'

sensor_harm.landsat_harmonize('LC8', sr_dir, target_dir)

end = time.time()
print(f'Duration time: {end - start}')
