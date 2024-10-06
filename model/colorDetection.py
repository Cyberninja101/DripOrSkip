from collections import Counter

import numpy as np
from kneed import KneeLocator
from sklearn.cluster import KMeans, HDBSCAN
from skimage.color import rgb2lab
import cv2
from cv2.gapi.wip.draw import Image

from PIL import Image
from rembg import remove, new_session
import matplotlib.pyplot as plt

import time
import json
import sys, os

sys.path.insert(1, os.path.join(os.getcwd(), "model"))

with open(os.path.join(os.getcwd(), "model", "colors.json"), 'r') as f:
    data = json.load(f)

hex_rgb_colors = list(data.keys())
rgb = np.dstack((np.asarray([int(hex[1:3], 16) for hex in hex_rgb_colors], np.uint8),
                 np.asarray([int(hex[3:5], 16) for hex in hex_rgb_colors], np.uint8),
                 np.asarray([int(hex[5:7], 16) for hex in hex_rgb_colors], np.uint8)))
lab = rgb2lab(rgb)

def getColors(imagePath):
    # Gets image into color array and resizes image
    image = cv2.cvtColor(cv2.imread(imagePath), cv2.COLOR_BGR2RGB)
    modImage = image.reshape(image.shape[0] * image.shape[1], 3)
    modImage = modImage[~np.all(modImage == [0, 0, 0], axis=1)]

    # Testing which values for n_clusters work best
    inertias = []
    for i in range(1,11):
        Kmeans = KMeans(n_clusters=i, max_iter=10, algorithm="lloyd")
        Kmeans.fit(modImage)
        inertias.append(Kmeans.inertia_)
    kneedle = KneeLocator([1,2,3,4,5,6,7,8,9,10], inertias, S=1.0, curve="convex", direction="decreasing")

    # Training the model
    clf = KMeans(n_clusters=kneedle.knee + 2, max_iter=500, algorithm="lloyd")
    labels = clf.fit_predict(modImage)
    centerColor = clf.cluster_centers_

    # Creates new dictionary based on the hexColors and the number of times they appear
    counts = Counter(labels)
    orderedColor = [centerColor[i] for i in counts.keys()]
    hexColors = [RGB2HEX(orderedColor[i]) for i in counts.keys()]
    colorMapping = dict(zip(hexColors, counts.values()))

    # Gets the closest color and maps to the value in the finalColorMapping dictionary
    finalColorMapping = dict()
    for color in hexColors:
        colorName = colorConverter(color)
        if(colorName in finalColorMapping):
            finalColorMapping[colorName] += colorMapping[color]
        elif colorName not in finalColorMapping:
            finalColorMapping[colorName] = colorMapping[color]

    # Removing garbage pixels and then turning everything into a percentile
    if "#000000" in finalColorMapping:
        del finalColorMapping["#000000"]

    totalPixels = 0
    totalPixels += np.sum(np.array(list(finalColorMapping.values())))

    keysArray = list(finalColorMapping.keys())
    for key in keysArray:
        finalColorMapping[key] = (finalColorMapping[key]/totalPixels)
        if(finalColorMapping[key] < 0.05):
             del finalColorMapping[key]

    print(finalColorMapping)
    # Turns it into a numpy array and returns it
    return finalColorMapping, keysArray

def colorConverter(hex_color):
    # Getting CIELAB colorings of the hex_color
    peaked_rgb = np.asarray([int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)], np.uint8)
    peaked_rgb = np.dstack((peaked_rgb[0], peaked_rgb[1], peaked_rgb[2]))
    peaked_lab = rgb2lab(peaked_rgb)

    # Finding the distances to all colors inside of the table
    lab_dist = np.sqrt(
        (lab[:, :, 0] - peaked_lab[:, :, 0])**2 + (lab[:, :, 1] - peaked_lab[:, :, 1])**2 + (lab[:, :, 2] - peaked_lab[:, :, 2])**2
    )

    # Get the index of the minimum distance
    min_index = lab_dist.argmin()
    peaked_closest_hex = hex_rgb_colors[min_index]

    # Returning the closest color hex code
    return peaked_closest_hex

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def denoise():
    image = cv2.imread("output.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def bgremove1(input_path): #8 seconds
    output_path = 'output.png'
    input = cv2.imread(input_path)
    input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)

    output = remove(input, session=new_session("u2netp"), bgcolor=(0, 0, 0, 255))
    blur = cv2.GaussianBlur(output, (21, 21), 0)
    # output.save(output_path)
    img = Image.fromarray(blur)
    img.show()

def promColors(colorDict, Ncolors=5):
    actualLength = min(len(colorDict), Ncolors)
    sortedColorDict = dict(sorted(colorDict.items(), key=lambda item: item[1], reverse=True))
    index = 0
    output = np.array([])
    for key in sortedColorDict.keys():
        output = np.append(output, np.array([data[key].replace("-", " ").capitalize(), str(round(sortedColorDict[key]*100, 2))]))
        index += 1
        if index == actualLength:
            break

    return output


def denoise():
    image = cv2.imread("output.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def bgremove1(input_path): #8 seconds
    output_path = 'output.png'
    input = Image.open(input_path)
    output = remove(input, bgcolor=(0, 0, 0, 255))
    output.save(output_path)

def bgremove2():
    print("fuck you")

if __name__ == '__main__':
    # function returns most prominent colors, with parameter n
    curr1 = time.time()
    colorDict, keys = getColors("output.png",20)
    output = promColors(colorDict)
    # print(colorDict)
    # print(keys)
    # print(output)
    curr2 = time.time()
    print("time to run ", curr2 - curr1)