import cv2
import numpy as np
from PIL import Image


def image_reflection(img):
    h = img.shape[0]
    w = img.shape[1]
    img_reflc = np.zeros((h, w))

    for y in range(h):
        for x in range(w):
            xf = (-1) * x + (w - 1)
            yf = y
            img_reflc[yf][xf] = img[y][x]

    return img_reflc


def image_rotation(img, deg):
    h = img.shape[0]
    w = img.shape[1]
    img_rot = np.zeros((h, w))
    deg = np.radians(deg)

    xs = int(w / 2)
    ys = int(h / 2)

    for y in range(ys, -1, -1):
        for x in range(xs, w):
            xp = xs + round(x * np.cos(deg) - y * np.sin(deg))
            yp = round(x * np.sin(deg) + y * np.cos(deg))

            try:
                img_rot[yp][xp] = img[y][x]
            except IndexError:
                pass

    for y in range(ys, -1, -1):
        for x in range(xs):
            xp = xs + round(x * np.cos(deg) - y * np.sin(deg))
            yp = round(x * np.sin(deg) + y * np.cos(deg))
            try:
                img_rot[yp][xp] = img[y][x]
            except IndexError:
                pass

    return img_rot


def image_projection(img):
    h = img.shape[0]
    w = img.shape[1]

    d = 0.1
    img_perspc = np.zeros((h, w))

    y_ref = h
    x_ref = round(w / 2)
    f = 150

    z = h
    for y in range(y_ref):
        for x in range(x_ref, w):
            x_perspc = x_ref + round((f * (x - x_ref)) / (z + f))
            y_perspc = round((f * h) / (z + f))

            try:
                img_perspc[y_perspc][x_perspc] = img[y][x]
            except IndexError:
                print(x_perspc)
        z = z - 1

    z = h
    for y in range(y_ref):
        for x in range(x_ref):
            x_perspc = x_ref + round((f * (x - x_ref)) / (z + f))
            y_perspc = round((f * h) / (z + f))

            try:
                img_perspc[y_perspc][x_perspc] = img[y][x]
            except IndexError:
                print(x_perspc)
        z = z - 1

    return img_perspc


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    path = r'chess-board.png'
    img = cv2.imread(path, 0)
    img = image_projection(img)
    img = Image.fromarray(img)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("perspective_img.jpg")

    path = r'perspective_img.jpg'
    img = cv2.imread(path, 0)
    img = image_rotation(img, deg=40)
    img = Image.fromarray(img)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("rotated_img.jpg")

    path = r'rotated_img.jpg'
    img = cv2.imread(path, 0)
    img = image_reflection(img)
    img = Image.fromarray(img)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("reflected_img.jpg")
