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

    pose = Rotation.from_matrix(rot)
    euler_angel = pose.as_euler("XYZ", degrees=True)

    r11, r12, r13 = rot[0][0], rot[0][1], rot[0][2]
    r21, r22, r23 = rot[1][0], rot[1][1], rot[1][2]
    r31, r32, r33 = rot[2][0], rot[2][1], rot[2][2]

    pitch = euler_angel[0]
    yaw = euler_angel[1]
    roll = euler_angel[2]

    # the code below just for show
    adjust_matrix = np.asarray([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ])
    rot = np.dot(adjust_matrix, rot)
    # end of the code

    length = 100
    rotation_mat = rot
    rotation_mat *= length

    x_start = (img.shape[1] // 2, img.shape[0] // 2)
    y_start = (img.shape[1] // 2, img.shape[0] // 2)
    z_start = (img.shape[1] // 2, img.shape[0] // 2)

    x_end = (x_start[0] + int(rotation_mat[0][0]),
             x_start[1] + int(rotation_mat[1][0]))
    y_end = (y_start[0] + int(rotation_mat[0][1]),
             y_start[1] + int(rotation_mat[1][1]))
    z_end = (z_start[0] + int(rotation_mat[0][2]),
             z_start[1] + int(rotation_mat[1][2]))

    cv2.putText(img, "pitch: " + str(round(pitch, 2)), (5, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(img, "yaw: " + str(round(yaw, 2)), (5, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img, "roll: " + str(round(roll, 2)), (5, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # red green blue for the x, y and z axis
    cv2.line(img, x_start, x_end, (0, 0, 255), 2)
    cv2.line(img, y_start, y_end, (0, 255, 0), 2)
    cv2.line(img, z_start, z_end, (255, 0, 0), 2)

    cv2.putText(img, str(round(r11, 2)), (370, 360),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)
    cv2.putText(img, str(round(r12, 2)), (470, 360),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)
    cv2.putText(img, str(round(r13, 2)), (570, 360),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)

    cv2.putText(img, str(round(r21, 2)), (370, 410),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)
    cv2.putText(img, str(round(r22, 2)), (470, 410),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)
    cv2.putText(img, str(round(r23, 2)), (570, 410),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)

    cv2.putText(img, str(round(r31, 2)), (370, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)
    cv2.putText(img, str(round(r32, 2)), (470, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)
    cv2.putText(img, str(round(r33, 2)), (570, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (32, 32, 200), 2)

    return img
