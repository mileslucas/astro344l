import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

# data = np.genfromtxt('data/tyco2regions.csv', skip_header=1)

df = pd.read_csv('data/tyco2regions.csv')

data = df[['x', 'y']].values
names = df['name']


from photutils import CircularAperture

pairs = []
for i, pair in enumerate(data):
    if pair[0] >=0 and pair[1] >= 0:
        pairs.append(pair)

pairs = np.array(pairs)

pairs[:, 1] = -1 * pairs[:, 1] + 510
apts = CircularAperture(pairs, r=12)

image = mpimg.imread('docs/figs/rgb_full.png')



plt.imshow(image, origin='lower')
apts.plot(color='g', alpha=1, lw=1)

flips = ['3152-1423-1', '3152-712-1', '3152-1451-1']

for pair, name in zip(pairs, names):
    loc = pair + 10
    if name in flips:
        loc = [pair[0] + 10, pair[1] - 10]

    plt.text(*loc, name, color='w', fontsize=6)

plt.box(on=None)
plt.axis('off')

plt.tight_layout()
width = 3.404 * 2
height = width * .9
plt.gcf().set_size_inches(width, height)
plt.savefig('docs/figs/map.pdf', transparent=True)
plt.show()
