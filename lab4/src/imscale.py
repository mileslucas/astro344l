'''
imscale.py

Author: Miles Lucas

This script parses the image scales of given images and reports a confidence interval. The images are expected to have been coordinate-mapped using koords so that the FITS headers match the keywords
'''

import numpy as np
from astropy.io import fits
from glob import glob
import sys
from scipy.stats import norm

def get_interval(data):
    ''' Reports the 95 percent confidence interval using normal distribution '''
    mu = np.average(data)
    stdev = np.std(data)
    alpha = .05
    min_, max_ = norm.interval(1-alpha, loc=mu, scale=stdev)
    range_ = max_ - min_
    #Convert from degrees/pixel into arcseconds/Pixel
    conv_fact = 3600
    # Return an item that is x +- s as opposed to [low, upp]
    return mu * conv_fact, range_/2 * conv_fact

def main(filenames):
    ''' gets the important data from all the headers '''
    # Load the headers and get the data
    hdrs = [fits.getheader(filename) for filename in filenames]
    key1, key2 = 'CDELT1', 'CDELT2'
    cdelt1 = [hdr[key1] for hdr in hdrs]
    cdelt2 = [hdr[key2] for hdr in hdrs]
    print(cdelt1, cdelt2)
    # Get and print the intervals
    inter1 = get_interval(cdelt1)
    inter2 = get_interval(cdelt2)
    print('Pixel Scale Axis 1: {}+-{}'.format(*inter1))
    print('Pixel Scale Axis 2: {}+-{}'.format(*inter2))

if __name__=='__main__':
    if not len(sys.argv) == 2:
        print('Wrong number of arguments\nUsage: imscale.py <folderpath>')
        sys.exit()

    folder = sys.argv[1]
    filenames = glob(folder + '/*.fits')
    main(filenames)
