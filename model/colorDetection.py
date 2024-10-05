import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab
from collections import Counter
import cv2
import json

def get_colors(imagePath, nColors=10):
    #Gets image into color array and resizes image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    modImage = image.reshape(image.shape[0] * image.shape[1], 3)

    #Gets clusters using K Means
    clf = KMeans(n_clusters=nColors)
    labels = clf.fit_predict(modImage)
    centerColor = clf.cluster_centers_

    #Creates new dictionary based on the hexColors and the number of times they appear
    counts = Counter(labels)
    orderedColor = [centerColor[i] for i in counts.keys()]
    hexColors = [RGB2HEX(orderedColor[i]) for i in counts.keys()]
    colorMapping = dict(zip(hexColors, counts.values()))

    #Opens the colors json file
    with open('colors.json', 'r') as f_in:
        data = json.load(f_in)

    #Instatiates every element of the final dictionary
    finalColorMapping = dict()
    for hex in data:
        finalColorMapping[data[hex]] = 0

    #Gets the closest color and maps to the value in the finalColorMapping dictionary
    for color in hexColors:
        colorName = hex2name(color)
        finalColorMapping[colorName] += colorMapping[color]

    #Turns it into a numpy array and returns it
    return np.array(list(finalColorMapping.values())).reshape(1, len(finalColorMapping))

def hex2name(hex_color):
    #Opens the colors json file
    with open('colors.json', 'r') as f:
        color_table = json.loads(f.read())

    hex_rgb_colors = list(color_table.keys())
    rgb = np.dstack((np.asarray([int(hex[1:3], 16) for hex in hex_rgb_colors], np.uint8), np.asarray([int(hex[3:5], 16) for hex in hex_rgb_colors], np.uint8), np.asarray([int(hex[5:7], 16) for hex in hex_rgb_colors], np.uint8)))
    lab = rgb2lab(rgb)

    peaked_rgb = np.asarray([int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)], np.uint8)
    peaked_rgb = np.dstack((peaked_rgb[0], peaked_rgb[1], peaked_rgb[2]))
    peaked_lab = rgb2lab(peaked_rgb)

    lab_dist = np.sqrt(
        (lab[:, :, 0] - peaked_lab[:, :, 0])**2 + (lab[:, :, 1] - peaked_lab[:, :, 1])**2 + (lab[:, :, 2] - peaked_lab[:, :, 2])**2
    )

    # Get the index of the minimum distance
    min_index = lab_dist.argmin()
    peaked_closest_hex = hex_rgb_colors[min_index]
    peaked_color_name = color_table[peaked_closest_hex]

    return peaked_color_name

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
