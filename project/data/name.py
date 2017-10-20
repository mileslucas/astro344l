from glob import glob
import os

def main():
    filenames = glob('*V*.FIT')
    na = len(os.listdir('a/'))
    nb = len(os.listdir('b/'))
    a, b = 67, 69
    for filename in reversed(filenames):
        base = filename[:-7]
        num = filename[-7:-4]
        ext = filename[-4:]
        os.rename(filename, base + str(int(num) + a + b) + ext)


if __name__=='__main__':
    main()
