from collections import Counter
import time

import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift


import cv2
import colorsys
from rembg import remove, new_session

def getColors(imagePath, trials = 25):
    # Preprocessing image
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.medianBlur(image, 3)
    image = remove(image, session=new_session("u2netp"), bgcolor=(0, 0, 0, 255))
    image = image[:, :, :3]
    cv2.imwrite("img1.png", image)
    modImage = image.reshape(image.shape[0] * image.shape[1], 3)
    modImage = modImage[~np.all(modImage == [0, 0, 0], axis=1)]
    cv2.imwrite("img2.png", modImage)

    allTrials = dict()
    for i in range(trials):
        # Creating too many clusters and then cleaning them up later through merging
        kmeans = KMeans(n_clusters=20, max_iter=500)
        labels = kmeans.fit_predict(modImage)
        centerColors = kmeans.cluster_centers_

        # We get ordered colors by iterating through the keys
        counts = Counter(labels)
        numbers = list(counts.values())
        orderedColors = [centerColors[i] for i in counts.keys()]
        hexColors = [RGB2HEX(orderedColors[i]) for i in counts.keys()]
        for i in range(len(hexColors)):
            if hexColors[i] in allTrials:
                allTrials[hexColors[i]] += numbers[i]
            else:
                allTrials[hexColors[i]] = numbers[i]

    # Getting the hue calculations
    hexColors = list(allTrials.keys())
    counts = list(allTrials.values())
    hues = []
    for color in hexColors:
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        hues.append(colorsys.rgb_to_hls(r, g, b)[0])
    # Finding the overall percentages of the pixel colors
    sum = np.sum(np.array(counts))
    prob = np.array(counts) / sum
    print(hues)

    # 1D Clustering Algorithm (Mean Shift)
    meanshift = MeanShift(max_iter=1000).fit(np.array(hues).reshape(-1, 1))
    clusters = meanshift.predict(np.array(hues).reshape(-1, 1))
    clusterCount = len(meanshift.cluster_centers_)

    # Getting the probability per cluster
    probCluster = [0] * clusterCount
    for i in range(len(hexColors)):
        probCluster[clusters[i]] += prob[i]

    # Getting the final color values
    finalColors = [[0, 0, 0]] * clusterCount
    for i in range(len(hexColors)):
        h = finalColors[clusters[i]][0]
        s = finalColors[clusters[i]][1]
        l = finalColors[clusters[i]][2]
        r = int(hexColors[i][1:3], 16) / 255
        g = int(hexColors[i][3:5], 16) / 255
        b = int(hexColors[i][5:7], 16) / 255
        pixel = colorsys.rgb_to_hls(r, g, b)
        finalColors[clusters[i]] = [h + ((pixel[0] * prob[i]) / probCluster[clusters[i]]),
                                    s + ((pixel[1] * prob[i]) / probCluster[clusters[i]]),
                                    l + ((pixel[2] * prob[i]) / probCluster[clusters[i]])]

    for i in range(clusterCount):
        pixel = colorsys.hls_to_rgb(finalColors[i][0], finalColors[i][1], finalColors[i][2])
        r = int(pixel[0] * 255)
        g = int(pixel[1] * 255)
        b = int(pixel[2] * 255)
        r = f"{r:02x}"
        g = f"{g:02x}"
        b = f"{b:02x}"
        finalColors[i] = "#" + r + g + b

    ColorsDict = dict(zip(finalColors, probCluster))
    return ColorsDict

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def promColors(colorDict):
    sortedColorDict = dict(sorted(colorDict.items(), key=lambda item: item[1], reverse=True))
    output = dict()
    threshold = 1/(len(sortedColorDict.values())*3.5)
    for key in sortedColorDict.keys():
        if(sortedColorDict[key] > threshold):
            output[key] = str(round(sortedColorDict[key]*100, 2))
    return output

if __name__ == '__main__':
    # function returns most prominent colors, with parameter n
    curr1 = time.time()
    colorDict = getColors("new (3).png")
    print(promColors(colorDict))
    curr2 = time.time()
    print("time to run ", curr2 - curr1)
