from collections import Counter

import numpy as np
from kneed import KneeLocator
from sklearn.cluster import KMeans, HDBSCAN
from skimage.color import rgb2lab
import cv2

from rembg import remove, new_session

import time
import json

with open('colors.json', 'r') as f:
    data = json.load(f)

hex_rgb_colors = list(data.keys())
rgb = np.dstack((np.asarray([int(hex[1:3], 16) for hex in hex_rgb_colors], np.uint8),
                 np.asarray([int(hex[3:5], 16) for hex in hex_rgb_colors], np.uint8),
                 np.asarray([int(hex[5:7], 16) for hex in hex_rgb_colors], np.uint8)))
lab = rgb2lab(rgb)

def getColors(imagePath, trials = 250):
    # Preprocessing image
    image = cv2.imread(imagePath)
    halfImage = cv2.resize(image, (0, 0), fx=0.1, fy=0.1)
    halfImage = cv2.cvtColor(halfImage, cv2.COLOR_BGR2RGB)
    output = remove(halfImage, session=new_session("u2netp"), bgcolor=(0, 0, 0, 255))
    output = output[:,:,:3]
    blur = cv2.medianBlur(output, 5)
    cv2.imwrite("img1.png", blur)
    modImage = blur.reshape(blur.shape[0] * blur.shape[1], 3)
    modImage = modImage[~np.all(modImage == [0, 0, 0], axis=1)]

    # Testing which values for n_clusters work best
    inertias = []
    for i in range(1,11):
        Kmeans = KMeans(n_clusters=i, max_iter=5)
        Kmeans.fit(modImage)
        inertias.append(Kmeans.inertia_)
    kneedle = KneeLocator([1,2,3,4,5,6,7,8,9,10], inertias, S=1.0, curve="convex", direction="decreasing")

    outputs = []
    for i in range(trials):
        # Training the model
        clf = KMeans(n_clusters=3*kneedle.knee, max_iter=1000)
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

        while(True):
            edited = False
            totalPixels = 0
            totalPixels += np.sum(np.array(list(finalColorMapping.values())))
            k = len(finalColorMapping.keys())
            keysArray = list(finalColorMapping.keys())
            for key in keysArray:
                finalColorMapping[key] = (finalColorMapping[key]/totalPixels)
                if finalColorMapping[key] < 1/(2*k):
                    del finalColorMapping[key]
                    edited = True
            if not edited:
                break

        outputs.append(finalColorMapping)

    outputDict = dict()
    for output in outputs:
        for key in output.keys():
            if key in outputDict:
                outputDict[key] += output[key]/trials
            else:
                outputDict[key] = output[key]/trials

    print(outputDict)
    # Turns it into a numpy array and returns it
    return outputDict

def colorConverter(hex_color):
    # Getting CIELAB colorings of the hex_color
    peaked_rgb = np.asarray([int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)], np.uint8)
    peaked_rgb = np.dstack((peaked_rgb[0], peaked_rgb[1], peaked_rgb[2]))
    peaked_lab = rgb2lab(peaked_rgb)

    # Finding the distances to all colors inside the table
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

def bgremove1(input_path, output_path): #8 seconds
    input = cv2.cvtColor(cv2.imread(input_path), cv2.COLOR_BGR2RGB)
    output = remove(input, session=new_session("u2net"), bgcolor=(0, 0, 0, 255))
    output.save(output_path)

def promColors(colorDict, threshold = 0.08):
    sortedColorDict = dict(sorted(colorDict.items(), key=lambda item: item[1], reverse=True))
    output = np.array([])
    for key in sortedColorDict.keys():
        if(sortedColorDict[key] > threshold):
            output = np.append(output, np.array([data[key].replace("-", " ").capitalize(), str(round(sortedColorDict[key]*100, 2))]))
    return output


if __name__ == '__main__':
    # function returns most prominent colors, with parameter n
    curr1 = time.time()
    colorDict = getColors("3.png")
    print(promColors(colorDict))
    curr2 = time.time()
    print("time to run ", curr2 - curr1)