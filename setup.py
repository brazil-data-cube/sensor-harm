from setuptools import find_packages, setup

packages = find_packages()

install_requires = [
    # 'GDAL',
    'numpy',
    'rasterio',
    's2angs @ git+https://github.com/brazil-data-cube/sentinel2_angle_bands'
]

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='sensor-harm',
    url='https://github.com/marujore/sensor-harm',
    author='Rennan Marujo',
    author_email='rennanmarujo@gmail.com',
    # Needed to actually package something
    packages=packages,
    # Needed for dependencies
    install_requires=install_requires,
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Script to calculate Generate Nadir BRDF Adjusted Reflectance',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
