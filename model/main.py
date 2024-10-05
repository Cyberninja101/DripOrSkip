import sys

import colorDetection, yolo, cvtcolor

def drip(image):
    path = yolo.crop_image(sys.path[0]+"/"+image)
    colorDetection.bgremove1(path)
    colorDict, keys = colorDetection.getColors("output.png",20)
    print(colorDict)
    print(keys)
    rgbs = [i[1:] for i in list(colorDict.keys())]
    rgbs.sort(key=lambda x: colorDict["#"+x], reverse=True)
    print(rgbs)
    hsls = []
    for i in rgbs:
        hsls.append(cvtcolor.rgb_to_hsl(int(i[:2], 16), int(i[2:4], 16), int(i[4:6], 16)))
    print(hsls)
    analogous_score, complimentary_score, split_score = 0, 0, 0
    if len(hsls) > 1:
        for i in range(1, len(hsls)):
            if (hsls[0][0] - 30) % 360 < hsls[i][0] < (hsls[0][0] + 30) % 360:
                analogous_score += 1
            elif (hsls[0][0] + 170) % 360 < hsls[i][0] < (hsls[0][0] + 190) % 360:
                complimentary_score += 1
            elif (hsls[0][0] + 145) % 360 < hsls[i][0] < (hsls[0][0] + 155) % 360:
                split_score += 1
            elif (hsls[0][0] + 205) % 360 < hsls[i][0] < (hsls[0][0] + 215) % 360:
                split_score += 1
    else:
        print("you made an outfit of one color how boring")
    return (len(hsls), analogous_score, complimentary_score, split_score)