from glob import glob

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
    pscale = np.mean(scales)
    pscale_std = np.std(scales)
    return pscale, std

def get_fov(pscale, std, dalpha, leng):
    fov = leng * pscale
    std = leng * pscale**2 / dalpha * std
    return fov, std

if __name__ == '__main__':
    filenames = glob('../data/science/processed/*V*tenth*')
    imgs = [fits.getdata(file) for file in filenames]
    seps = [get_sep(img) for img in imgs]
    dalpha = 35.3
    pscale = get_pscale(seps, dalpha)
    x_len, y_len = imgs[0].T.shape
    fovx = get_fov(*pscale, dalpha, x_len)
    fovy = get_fov(*pscale, dalpha, y_len)

    print(pscale)
    print(fovx)
    print(fovy)
