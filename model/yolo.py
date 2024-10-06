import sys
import cv2
from ultralytics import YOLO
from face_detector import YoloDetector
import numpy as np
from PIL import Image


def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] *
             (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)


def crop_image(file: str):
    model = YoloDetector(target_size=720, device="cpu", min_face=90)
    image = Image.open(sys.path[0] + "/" + file)
    image = image.convert("RGB")
    image = np.asarray(image, dtype=np.float32) / 255
    image = image[:,:,:3]
    orgimg = image
    bboxes, points = model.predict(orgimg)
    yolo = YOLO('yolov5s.pt')
    image = cv2.imread(sys.path[0] + "/" + file, 1)
    finalimage = Image.open(sys.path[0] + "/" + file)

    results = yolo.track(image)
    boxreal = None
    [x1, y1, x2, y2] = [0, 0, 0, 0]
    for result in results:
        # get the classes names
        classes_names = result.names

        # iterate over each box
        for box in result.boxes:
            if box.conf[0] > 0.4 and int(box.cls[0]) == 0:
                [a, b, c, d] = [int(i) for i in box.xyxy[0]]
                if (c - a) * (d - b) > (x2 - x1) * (y2 - y1):
                    [x1, y1, x2, y2] = [a, b, c, d]
                    boxreal = box

        # get coordinates
        [x1, y1, x2, y2] = boxreal.xyxy[0]
        # convert to int
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # get the class
        cls = int(boxreal.cls[0])

        # get the class name
        class_name = classes_names[cls]

        # get the respective colour
        colour = getColours(cls)

        # draw the rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), colour, 2)
        cv2.imwrite("croptest.png", image)
        for j in bboxes[0]:
            if j[3] > y1 and j[2] < x2 and j[0] > x1:
                y1 = j[3]
                cv2.rectangle(image, (j[0], j[1]), (j[2], j[3]), colour, 2)
        
        finalimage = finalimage.crop((x1, y1, x2, y2))

        # put the class name and confidence on the image
        cv2.putText(image, f'{classes_names[int(boxreal.cls[0])]} {box.conf[0]:.2f}', (x1, y1),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)

    finalimage.save(sys.path[0] + "/new.png")
    return sys.path[0] + "/new.png"