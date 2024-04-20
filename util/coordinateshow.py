import cv2
from scipy.spatial.transform import Rotation
import numpy as np

"""
the first method to draw a axis:
head coordinate:
y
-
-
-
-
o-------->x

but in the image:
x--------->x
-
-
-
-
y

so the transform mat are
[1, 0,  0
 0, -1, 0
 0, 0, -1]
"""


def draw_axis_on_img(img, rot):
    assert img.shape == (480, 640, 3)
    length = 100
    rotation_mat = rot
    rotation_mat *= length
    rot_ic = np.asarray([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ])
    rotation_mat = np.dot(rot_ic, rotation_mat)

    x_start = (img.shape[1] // 2, img.shape[0] // 2)
    y_start = (img.shape[1] // 2, img.shape[0] // 2)
    z_start = (img.shape[1] // 2, img.shape[0] // 2)

    x_end = (x_start[0] + int(rotation_mat[0][0]),
             x_start[1] + int(rotation_mat[1][0]))
    y_end = (y_start[0] + int(rotation_mat[0][1]),
             y_start[1] + int(rotation_mat[1][1]))
    z_end = (z_start[0] + int(rotation_mat[0][2]),
             z_start[1] + int(rotation_mat[1][2]))

    # red green blue for the x, y and z axis
    cv2.line(img, x_start, x_end, (0, 0, 255), 2)
    cv2.line(img, y_start, y_end, (0, 255, 0), 2)
    cv2.line(img, z_start, z_end, (255, 0, 0), 2)

    return img
