from astropy.io import fits
from astropy.time import Time
import pandas as pd
from glob import glob

def main():
    filenames = glob('../data/*.fts')
    hdrs = [fits.getheader(filename) for filename in filenames]
    dates = [hdr['Date'] for hdr in hdrs]
    times = [hdr['date_obs'].split(' ')[-1] for hdr in hdrs]
    astro_times = [Time(date + ' ' + time, format='iso') for date, time in zip(dates, times)]
    mjd_times = [t.mjd for t in astro_times]
    df = pd.DataFrame()
    df['Date'] = dates
    df['Time'] = times
    df['MJD'] = mjd_times
    df.to_csv('table.csv')


if __name__=='__main__':
    main()
