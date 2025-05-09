import os
from glob import glob
import numpy as np
from tifffile import imread, imwrite

def reslize_movie(movie, dx=1):
    T,size_y,size_x = movie.shape
    slices = np.zeros((size_x//dx, T, size_y), dtype=movie.dtype)
    for x in range(0,size_x, dx):
        slice = movie[:, :, x]
        slices[x//dx, :, :] = slice
    return slices

# get a list of all filenames ending in .tif using glob
subfolder = 'data_batch_01'
filenames = glob(subfolder+'/*.tif')
filenames.sort()
for j,fn in enumerate(filenames): 
    movie = imread(fn)
    slices = reslize_movie(movie)
    # save the resliced data
    imwrite(subfolder+f'/resliced_{j:03d}.tif', slices, photometric='minisblack')
    print(f'Processed {fn} - saved as {subfolder+f"/resliced_{j:03d}.tif"}')