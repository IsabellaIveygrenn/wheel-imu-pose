import cv2
import numpy as np
from scipy.spatial.transform import Rotation
from util.coordinateshow import draw_axis_on_img
import copy

from util.detectPort import open_port
from util.realport import read_stream_from_port

# setting of the record
isInitialed = False
isCollected = True

"""initialization of the r1 state"""
r1 = np.identity(3)


"""
try to open the port
"""
serial_ = open_port()
cap = cv2.VideoCapture(0)


while isCollected:

    quat_from_f = read_stream_from_port(serial_)
    if quat_from_f is None:
        continue
    q_x, q_y, q_z, q_w = quat_from_f[0], quat_from_f[1], quat_from_f[2], quat_from_f[3]
    abs_pose_mat = Rotation.from_quat([q_x, q_y, q_z, q_w]).as_matrix()

    ret, frame = cap.read()

    if isInitialed:
        rel_pose_mat = np.dot(np.linalg.inv(r1), abs_pose_mat)
        frame_axis = draw_axis_on_img(frame, rel_pose_mat)
    else:
        frame_axis = draw_axis_on_img(frame, np.identity(3))

    cv2.imshow("video streamS", frame_axis)
    command = cv2.waitKey(10)
    if command == ord('e'):
        isCollected = False
    elif command == ord('i'):
        print('begin the calibration')
        r1 = abs_pose_mat
        isInitialed = True
        print('end the calibration')
    else:
        continue


print("the program has done all the control flow")
