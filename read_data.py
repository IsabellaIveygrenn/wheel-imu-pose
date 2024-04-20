import cv2
import numpy as np
import sys
from scipy.spatial.transform import Rotation
from util.coordinateshow import draw_axis_on_img
import copy

import serial  # 导入模块
import serial.tools.list_ports
import threading
import struct
import time
import platform
# from copy import deepcopy
# import os
# import math
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from util.detectPort import open_port


# 宏定义参数
PI = 3.1415926
FRAME_HEAD = str('fc')
FRAME_END = str('fd')
TYPE_IMU = str('40')
TYPE_AHRS = str('41')
TYPE_INSGPS = str('42')
TYPE_GEODETIC_POS = str('5c')
TYPE_GROUND = str('f0')
TYPE_SYS_STATE = str('50')
TYPE_BODY_ACCELERATION = str('62')
TYPE_ACCELERATION = str('61')
IMU_LEN = str('38')  # //56
AHRS_LEN = str('30')  # //48
INSGPS_LEN = str('48')  # //72
GEODETIC_POS_LEN = str('20')  # //32
SYS_STATE_LEN = str('64')  # // 100
BODY_ACCELERATION_LEN = str('10')  # // 16
ACCELERATION_LEN = str('0c')  # 12
PI = 3.141592653589793
DEG_TO_RAD = 0.017453292519943295
isrun = True

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

    check_head = serial_.read().hex()
    if check_head != FRAME_HEAD:
        continue
    head_type = serial_.read().hex()
    if (head_type != TYPE_IMU and head_type != TYPE_AHRS and head_type != TYPE_INSGPS and
        head_type != TYPE_GEODETIC_POS and head_type != 0x50 and head_type != TYPE_GROUND and
        head_type != TYPE_SYS_STATE and head_type != TYPE_BODY_ACCELERATION and
            head_type != TYPE_ACCELERATION):
        continue
    check_len = serial_.read().hex()
    # 校验数据类型的长度
    if head_type == TYPE_IMU and check_len != IMU_LEN:
        continue
    elif head_type == TYPE_AHRS and check_len != AHRS_LEN:
        continue
    elif head_type == TYPE_INSGPS and check_len != INSGPS_LEN:
        continue
    elif head_type == TYPE_GEODETIC_POS and check_len != GEODETIC_POS_LEN:
        continue
    elif head_type == TYPE_SYS_STATE and check_len != SYS_STATE_LEN:
        continue
    elif head_type == TYPE_GROUND or head_type == 0x50:
        continue
    elif head_type == TYPE_BODY_ACCELERATION and check_len != BODY_ACCELERATION_LEN:
        print("check head type "+str(TYPE_BODY_ACCELERATION) +
              " failed;"+" check_LEN:"+str(check_len))
        continue
    elif head_type == TYPE_ACCELERATION and check_len != ACCELERATION_LEN:
        print("check head type "+str(TYPE_ACCELERATION) +
              " failed;"+" ckeck_LEN:"+str(check_len))
        continue
    check_sn = serial_.read().hex()
    head_crc8 = serial_.read().hex()
    crc16_H_s = serial_.read().hex()
    crc16_L_s = serial_.read().hex()
    if head_type == TYPE_AHRS:
        # print("read the data correctly")
        data_s = serial_.read(int(AHRS_LEN, 16))
        AHRS_DATA = struct.unpack('10f ii', data_s[0:48])
        q_w = AHRS_DATA[6]
        q_x = AHRS_DATA[7]
        q_y = AHRS_DATA[8]
        q_z = AHRS_DATA[9]
    else:
        continue

    abs_pose = Rotation.from_quat([q_x, q_y, q_z, q_w])
    abs_pose_mat = abs_pose.as_matrix()

    if isInitialed:
        # a = np.asarray([
        #     [0, 0, 1],
        #     [1, 0, 0],
        #     [0, 1,0]
        # ])
        rel_pose_mat = np.dot(np.linalg.inv(r1), abs_pose_mat)
        print(r1)
        print(abs_pose.as_quat())

    ret, frame = cap.read()
    if isInitialed:
        # print(type(r1))
        cpy_r1 = copy.deepcopy(r1)
        # a = np.asarray([
        #     [0, 0, -1],
        #     [0, -1, 0],
        #     [-1, 0, 0]
        # ])
        frame_axis = draw_axis_on_img(frame, rel_pose_mat)
    else:
        frame_axis = draw_axis_on_img(frame, np.identity(3))

    cv2.imshow("video stream", frame_axis)
    command = cv2.waitKey(3)

    if command == ord('e'):
        isCollected = False
    elif command == ord('i'):
        print('begin the calibration')
        print(abs_pose.as_quat)
        r1 = abs_pose_mat
        print(np.linalg.det(r1))
        isInitialed = True
        print('end the calibration')
    else:
        continue


print("the program has done all the things")
