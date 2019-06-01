#!/bin/env python3
__description__ = '''
This is a way to load whole slide images (WSI) and sections of them.
Fully working on linux.
Dependencies:
    - Curl
    - HistomicsTK (can be installed with pip)
    - libtiff
    - openslide
More info: https://digitalslidearchive.github.io/HistomicsTK/examples/wsi-io-using-large-image.html
'''
__author__ = 'Santiago Smith Silva'
__year__ = 2019


import os
from os.path import join, isfile

import skimage
import large_image
import matplotlib.pyplot as plt

# Some nice default configuration for plots
plt.rcParams['figure.figsize'] = 10, 10
plt.rcParams['image.cmap'] = 'gray'

if __name__ == '__main__':
    wsi_url = 'https://data.kitware.com/api/v1/file/5899dd6d8d777f07219fcb23/download'
    # wsi_path = 'TCGA-02-0010-01Z-00-DX4.07de2e55-a8fe-40ee-9e98-bcb78050b9f7.svs'
    wsi_path = '/home/ssilvari/Downloads/gdc_download_20190601_163159.029299/eec8e8a2-48d6-4875-bfb4-9e815c6a76d4' \
               '/TCGA-QR-A6ZZ-01Z-00-DX1.4B26C454-0C23-4072-BD5A-35438032B5F2.svs'
    assert isfile(wsi_path), 'File not found'

    if not isfile(wsi_path):
        print('WSI not found. Downloading it from TCGA...')
        os.system(f'curl -OJ {wsi_url}')

    print(f'Loading WSI: {wsi_path} ...')
    ts = large_image.getTileSource(wsi_path)  # Loads several formats - Based on OpenSlide

    print(f'Image Metadata:')
    metadata = ts.getMetadata()
    for key, value in metadata.items():
        print(f'\t- {key}: {value}')

    # Get the magnification associated with all levels of the image pyramid
    print('Info at each level of the image pyramid:')
    for i in range(ts.levels):
        print('Level {} : {}'.format(
            i, ts.getMagnificationForLevel(level=i)))

    # Set the magnification level (Zoom) (e.g. 20X)
    print(f'Native magnification: {ts.getNativeMagnification()}')
    mag_level = ts.getNativeMagnification()['magnification']
    level = ts.getLevelForMagnification(mag_level)  # Get which level correspond to that magnification
    print(f'Level {level} corresponds to a magnification of: {mag_level}X')

    # Get a tile (patch)
    pos = 600  # Position
    tile_info = ts.getSingleTile(
        tile_size=dict(width=1790, height=1046),
        scale=dict(magnification=mag_level),
        tile_position=pos
    )

    plt.imshow(tile_info['tile'])
    plt.show()

    skimage.io.imsave('slide.png', tile_info['tile'])

