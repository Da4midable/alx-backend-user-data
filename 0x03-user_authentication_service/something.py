from PIL import Image

Image.open('naruto.jpeg')

import numpy as np
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import KMeans

image = mpimg.imread('naruto.jpeg')
w, h, d = image.shape
pixels = image.reshape(w * h, d)
n_colors = 10
kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(pixels)
palette = np.uint8(kmeans.cluster_centers_)
plt.imshow([palette])
plt.axis('off')
plt.show()
