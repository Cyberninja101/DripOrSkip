import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab
from collections import Counter
import cv2
import time
import json

with open('colors.json', 'r') as f:
    data = json.load(f)

hex_rgb_colors = list(data.keys())
rgb = np.dstack((np.asarray([int(hex[1:3], 16) for hex in hex_rgb_colors], np.uint8),
                 np.asarray([int(hex[3:5], 16) for hex in hex_rgb_colors], np.uint8),
                 np.asarray([int(hex[5:7], 16) for hex in hex_rgb_colors], np.uint8)))
lab = rgb2lab(rgb)


def getColors(imagePath, nColors=8):
    # Gets image into color array and resizes image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    modImage = image.reshape(image.shape[0] * image.shape[1], 3)
    # modImage = modImage[modImage != [0,0,0]]

    # Gets clusters using K Means
    clf = KMeans(n_clusters=nColors)
    labels = clf.fit_predict(modImage)
    centerColor = clf.cluster_centers_

    # Creates new dictionary based on the hexColors and the number of times they appear
    counts = Counter(labels)
    orderedColor = [centerColor[i] for i in counts.keys()]
    hexColors = [RGB2HEX(orderedColor[i]) for i in counts.keys()]
    colorMapping = dict(zip(hexColors, counts.values()))

    # Gets the closest color and maps to the value in the finalColorMapping dictionary
    finalColorMapping = dict()
    keysArray = []
    for color in hexColors:
        colorName = colorConverter(color)
        if (colorName in colorMapping):
            finalColorMapping[colorName] += colorMapping[color]
        elif colorName not in colorMapping and colorName != "#FFFF00":
            finalColorMapping[colorName] = colorMapping[color]
            keysArray.append(colorName)

    # Removing garbage pixels and then turning everything into a percentile
    if "#FFFF00" in finalColorMapping:
        del finalColorMapping["#FFFF00"]

    totalPixels = 0
    totalPixels += np.sum(np.array(list(finalColorMapping.values())))

    for key in keysArray:
        finalColorMapping[key] = (finalColorMapping[key] / totalPixels)
        if (finalColorMapping[key] < 0.05):
            del finalColorMapping[key]

    # Turns it into a numpy array and returns it
    return finalColorMapping, keysArray


def colorConverter(hex_color):
    # Getting CIELAB colorings of the hex_color
    peaked_rgb = np.asarray([int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)], np.uint8)
    peaked_rgb = np.dstack((peaked_rgb[0], peaked_rgb[1], peaked_rgb[2]))
    peaked_lab = rgb2lab(peaked_rgb)

    # Finding the distances to all colors inside of the table
    lab_dist = np.sqrt(
        (lab[:, :, 0] - peaked_lab[:, :, 0]) ** 2 + (lab[:, :, 1] - peaked_lab[:, :, 1]) ** 2 + (
                    lab[:, :, 2] - peaked_lab[:, :, 2]) ** 2
    )

    # Get the index of the minimum distance
    min_index = lab_dist.argmin()
    peaked_closest_hex = hex_rgb_colors[min_index]

    # Returning the closest color hex code
    return peaked_closest_hex


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# function returns most prominent colors, with parameter n
curr1 = time.time()
colorDict, keys = getColors("output.png", 20)
curr2 = time.time()
print("time to run ", curr2 - curr1)