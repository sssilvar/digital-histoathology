#!/bin/env python3
__description__ = '''
This is a way to load whole slide images (WSI) and sections of them.
Fully working on linux.
Dependencies:
    - Curl
    - HistomicsTK
'''

import os
from os.path import join, isfile

import large_image
import matplotlib.pyplot as plt

# Some nice default configuration for plots
plt.rcParams['figure.figsize'] = 10, 10
plt.rcParams['image.cmap'] = 'gray'

if __name__ == '__main__':
    wsi_url = 'https://data.kitware.com/api/v1/file/5899dd6d8d777f07219fcb23/download'
    wsi_path = 'TCGA-02-0010-01Z-00-DX4.07de2e55-a8fe-40ee-9e98-bcb78050b9f7.svs'

