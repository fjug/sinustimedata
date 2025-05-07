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
filenames = glob('*.tif')
for fn in filenames:
    movie = imread(fn)
    slices = reslize_movie(movie)
    # create a folder with the same name as the file
    folder = fn.split('.')[0]
    # create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # save the slices in the folder
    for i in range(slices.shape[0]):
        imwrite(os.path.join(folder, f'slice_{i}.tif'), slices[i], photometric='minisblack')