import serial  # 导入模块
import serial.tools.list_ports
import threading
import struct
import time
import platform
# from copy import deepcopy
# import sys
# import os
# import math

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

"""default setting of the entire program"""
port_option = 'COM4'
port_baudrate = 921600
port_timeout = 20


"""
check whether the port exist or not
if exist 
then open it with the config in the above and return a serial port
else return false throw an error and return None
"""


def find_serial():
    port_list = list(serial.tools.list_ports.comports())
    for port in port_list:
        if port.device == port_option:
            return True
    return False


def open_port():
    if not find_serial():
        return None
    serial_ = serial.Serial(port=port_option, baudrate=port_baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE,
                            stopbits=STOPBITS_ONE,
                            timeout=port_timeout)
    return serial_
