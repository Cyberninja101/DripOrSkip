import colorDetection, yolo, cvtcolor

path = yolo.crop_image("jasondataset.jpg")
colorDetection.bgremove1(path)
colorDict, keys = colorDetection.getColors("output.png",20)
print(colorDict)
print(keys)
rgbs = [i[1:] for i in list(colorDict.keys())]
print(rgbs)
hsls = []
for i in rgbs:
    hsls.append(cvtcolor.rgb_to_hsl(int(i[:2], 16), int(i[2:4], 16), int(i[4:6], 16)))
analogous_score, complimentary_score, split_score = 0, 0, 0;
if len(hsls) > 1:
    for i in range(len(hsls), -1, -1):
        if hsls[i][0] > hsls[-1][0] - 30 or hsls[i][0] < hsls[-1][0] + 30:
            analogous_score += 1
        elif hsls[i][0] > (hsls[-1][0] + 170) % 360 or hsls[i][0] < (hsls[-1][0] + 190) % 360:
            complimentary_score += 1
else:
    print("you made an outfit of one color how boring")