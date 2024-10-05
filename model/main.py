import colorDetection, yolo, cvtcolor

path = yolo.crop_image("jasondataset.jpg")
colorDetection.bgremove1(path)
colorDict, keys = colorDetection.getColors("output.png",20)
print(colorDict)
print(keys)
rgbs = [i[1:] for i in list(colorDict.keys())]
print(rgbs)