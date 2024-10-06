import sys, os

import colorDetection, yolo, cvtcolor
from PIL import Image

path = os.getcwd()



def check_analogous(base, compare):
    lower = base[0] - 30
    upper = base[0] + 30
    lower2 = lower + 360
    upper2 = upper + 360
    if lower < compare[0] < upper:
        return 1
    elif lower2 < compare[0] < upper2:
        return 1
    return 0


def check_complimentary(base, compare):
    lower = base[0] + 170
    upper = base[0] + 190
    if lower < 360 and upper > 360:
        if lower < compare[0] < 360 or compare[0] < upper-360:
            return 1
    elif lower > 360 and upper > 360:
        lower -= 360
        upper -= 360
    if lower < compare[0] < upper:
        return 1
    return 0


def check_split(base, compare):
    lower = base[0] + 145
    upper = base[0] + 155
    if lower < 360 and upper > 360:
        if lower < compare[0] < 360 or compare[0] < upper - 360:
            return 1
    elif lower > 360 and upper > 360:
        lower -= 360
        upper -= 360
    if lower < compare[0] < upper:
        return 1
    lower = base[0] + 205
    upper = base[0] + 215
    if lower < 360 and upper > 360:
        if lower < compare[0] < 360 or compare[0] < upper - 360:
            return 1
    elif lower > 360 and upper > 360:
        lower -= 360
        upper -= 360
    if lower < compare[0] < upper:
        return 1
    return 0


def drip(image):
    """
    :param image: file to check
    :return: an arr of length 2: first element is a tuple of nums (number of colors, analogous score, complimentary
             score, split complimentary score), second element is a dictionary of all the colors
    """

    path = yolo.crop_image(image)
    # changed to web_app/
    colorDict = colorDetection.getColors("web_app/new.png")
    promColorArr = colorDetection.promColors(colorDict)
    print(colorDict)
    print(promColorArr)
    rgbs = [i[1:] for i in promColorArr]
    rgbs.sort(key=lambda x: colorDict["#"+x], reverse=True)
    print(rgbs)
    hsls = []
    for i in rgbs:
        hsls.append(cvtcolor.rgb_to_hsl(int(i[:2], 16), int(i[2:4], 16), int(i[4:6], 16)))
    print(hsls)
    analogous_score, complimentary_score, split_score = 0, 0, 0

    for j in range(1, len(hsls)):
        analogous_score += check_analogous(hsls[0], hsls[j])
        complimentary_score += check_complimentary(hsls[0], hsls[j])
        split_score += check_split(hsls[0], hsls[j])
    # for i in range(len(hsls)):
    #     for j in range(i, len(hsls)):
    #         if i == j:
    #             continue
    #         analogous_score += check_analogous(hsls[i], hsls[j])
    #         complimentary_score += check_complimentary(hsls[i], hsls[j])
    #         split_score += check_split(hsls[i], hsls[j])
    return [(len(hsls), analogous_score, complimentary_score, split_score), promColorArr]


if __name__ == "__main__":
    print(drip("canvas_image.png"))