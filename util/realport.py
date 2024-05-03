import serial
import serial.tools.list_ports
import struct
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE


# predifine some configuration parameters
FRAME_HEAD = str('fc')
TYPE_IMU = str('40')
TYPE_AHRS = str('41')
TYPE_INSGPS = str('42')
TYPE_GEODETIC_POS = str('5c')
TYPE_GROUND = str('f0')
TYPE_SYS_STATE = str('50')
TYPE_BODY_ACCELERATION = str('62')
TYPE_ACCELERATION = str('61')
AHRS_LEN = str('30')  # //48


def read_stream_from_port(_serial):
    """
    check the serial read
    """
    check_head = _serial.read().hex()
    if check_head != FRAME_HEAD:
        return None
    head_type = _serial.read().hex()
    if head_type != TYPE_AHRS:
        return None
    check_len = _serial.read().hex()
    if check_len != AHRS_LEN:
        return None

    check_sn = _serial.read().hex()
    head_crc8 = _serial.read().hex()
    crc16_H_s = _serial.read().hex()
    crc16_L_s = _serial.read().hex()

    data_s = _serial.read(int(AHRS_LEN, 16))
    AHRS_DATA = struct.unpack('10f ii', data_s[0:48])
    q_w = AHRS_DATA[6]
    q_x = AHRS_DATA[7]
    q_y = AHRS_DATA[8]
    q_z = AHRS_DATA[9]

    return [q_x, q_y, q_z, q_w]
