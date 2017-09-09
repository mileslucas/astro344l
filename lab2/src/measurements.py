from glob import glob
import argparse

import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils import DAOStarFinder


def get_sep(img):
    mean, median, std = sigma_clipped_stats(img, iters=5)
    daofind = DAOStarFinder(fwhm=3.0, threshold=5. * std)
    sources = daofind(img)
    positions = np.array([sources['xcentroid'], sources['ycentroid']]).T
    return np.linalg.norm(positions[0] - positions[1])

def get_pscale(seps, dalpha):
    pscales = dalpha / np.array(seps)
    pscale = np.mean(pscales)
    pscale_std = np.std(pscales)
    return pscale, pscale_std

def get_fov(pscale, std, dalpha, leng):
    fov = leng * pscale
    std = leng * pscale**2 / dalpha * std
    return fov, std

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Gets measurements from fits files')
    parser.add_argument('filename', help='files to process')
    args = parser.parse_args()
    filenames = glob(args.filename)
    imgs = [fits.getdata(files) for files in filenames]
    seps = [get_sep(img) for img in imgs]
    dalpha = 35.3
    pscale = get_pscale(seps, dalpha)
    x_len, y_len = imgs[0].T.shape
    fovx = get_fov(*pscale, dalpha, x_len)
    fovy = get_fov(*pscale, dalpha, y_len)

    print(pscale)
    print(fovx)
    print(fovy)
