import astropy.io.fits as pyfits
import numpy as np
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Create Median Dark Frames')
    parser.add_argument('base', help='The filename structure (ie without numbering)')
    parser.add_argument('num', type=int, help='The number of frames')
    parser.add_argument('output', help='The output filename')

    args = parser.parse_args()

    names = ['{}{:03d}.FIT'.format(args.base, n) for n in range(1, args.num + 1)]
    dark_frames = [pyfits.getdata(name).astype('f8') for name in names]
    median = np.median(dark_frames, axis=0)

    pyfits.writeto(args.output, median)
