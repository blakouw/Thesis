import os
from ctypes import *
from collections import namedtuple
from node_list import *
from time import sleep

"""
Kod producenta Virdyn
"""

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(PROJECT_ROOT, 'VDMocapSDK_DataRead.dll')
vdm = CDLL(path)

SensorState = namedtuple('SensorState', [
    'SS_NONE',
    'SS_Well',
    'SS_NoData',
    'SS_UnReady',
    'SS_BadMag',
])._make(range(5))

WorldSpace = namedtuple('WorldSpace', [
    'WS_Geo',
    'WS_Unity',
    'WS_UE4',
])(0, 1, 2)

CharSet = namedtuple('CharSet', [
    'CHAR_AUTO',
    'CHAR_UTF5',
])(0, 1)

BvhFormat = namedtuple('BvhFormat', [
    'BVH_Biovision_BVH',
    'BVH_3ds_max_biped',
])(0, 1)

RotationOrder = namedtuple('RotationOrder', [
    'RO_ZYX',
    'RO_ZXY',
    'RO_YZX',
    'RO_YXZ',
    'RO_XYZ',
    'RO_XZY',
])._make(range(6))

FbxFormat = namedtuple('FbxFormat', [
    'FBX_binary',
    'FBX_ascii',
    'FBX_encrypted',
    'FBX_6_0_binary',
    'FBX_6_0_ascii',
    'FBX_6_0_encrypted',
])._make(range(6))

OperationState = namedtuple('OperationState', [
    'OS_Un',
    'OS_Start',
    'OS_On',
    'OS_Fail',
    'OS_Success',
])._make(range(5))


class OperationProgress(Structure):
    _fileds_ = [
        ("state", OperationState),
        ("progress", c_float)
    ]


class MocapData(Structure):
    _fields_ = [
        ("isUpdate", c_bool),
        ("frameIndex", c_uint),
        ("frequency", c_int),
        ("nsResult", c_int),

        ("sensorState_body", c_uint * len(BodyNodes)),
        ("position_body", c_float * 3 * len(BodyNodes)),
        ("quaternion_body", c_float * 4 * len(BodyNodes)),
        ("gyr_body", c_float * 3 * len(BodyNodes)),
        ("acc_body", c_float * 3 * len(BodyNodes)),
        ("velocity_body", c_float * 3 * len(BodyNodes)),

        ("sensorState_rHand", c_uint * len(HandNodes_20_r)),
        ("position_rHand", c_float * 3 * len(HandNodes_20_r)),
        ("quaternion_rHand", c_float * 4 * len(HandNodes_20_r)),
        ("gyr_rHand", c_float * 3 * len(HandNodes_20_r)),
        ("acc_rHand", c_float * 3 * len(HandNodes_20_r)),
        ("velocity_rHand", c_float * 3 * len(HandNodes_20_r)),

        ("sensorState_lHand", c_uint * len(HandNodes_20_l)),
        ("position_lHand", c_float * 3 * len(HandNodes_20_l)),
        ("quaternion_lHand", c_float * 4 * len(HandNodes_20_l)),
        ("gyr_lHand", c_float * 3 * len(HandNodes_20_l)),
        ("acc_lHand", c_float * 3 * len(HandNodes_20_l)),
        ("velocity_lHand", c_float * 3 * len(HandNodes_20_l)),

        ("isUseFaceBlendShapesARKit", c_bool),
        ("isUseFaceBlendShapesAudio", c_bool),
        ("faceBlendShapesARKit", c_float * 52),
        ("faceBlendShapesAudio", c_float * 26),
        ("localQuat_RightEyeball", c_float * 4),
        ("localQuat_LeftEyeball", c_float * 4)
    ]


class Version(Structure):
    _fields_ = [
        ("Project_Name", c_ubyte*26),
        ("Author_Organization", c_ubyte*128),
        ("Author_Domain", c_ubyte*26),
        ("Author_Maintainer", c_ubyte*26),
        ("Version", c_ubyte*26),
        ("Version_Major", c_ubyte),
        ("Version_Minor", c_ubyte),
        ("Version_Patch", c_ubyte)
    ]


def get_version(ver):
    vdm.GetVerisonInfo(byref(ver))


def udp_set_position_in_initial_tpose(index, ip, port, ws, body, r_hand, l_hand):
    index = c_int(index)
    ip = create_string_buffer(ip.encode('gbk'), 30)
    port = c_ushort(port)
    ws = c_int(ws)
    type_float_array_3 = c_float * 3
    type_float_array_3_23 = type_float_array_3 * 23
    type_float_array_3_20 = type_float_array_3 * 20
    c_body = type_float_array_3_23()
    c_lhand = type_float_array_3_20()
    c_rhand = type_float_array_3_20()
    for i in range(len(body)):
        for j in range(len(body[0])):
            c_body[i][j] = c_float(body[i][j])
    for i in range(len(r_hand)):
        for j in range(len(r_hand[0])):
            c_rhand[i][j] = c_float(r_hand[i][j])
            c_lhand[i][j] = c_float(l_hand[i][j])

    vdm.UdpSetPositionInInitialTpose.restype = c_bool
    res = vdm.UdpSetPositionInInitialTpose(index, ip, port, ws, c_body, c_rhand, c_lhand)
    return bool(res)


def udp_open(index, port):
    index = c_int(index)
    vdm.UdpOpen.restype = c_bool
    res = vdm.UdpOpen(index, port)
    sleep(0.1)
    return bool(res)


def udp_close(index):
    sleep(0.1)
    index = c_int(index)
    vdm.UdpClose(index)


def udp_is_open(index):
    index = c_int(index)
    vdm.UdpIsOpen.restype = c_bool
    res = vdm.UdpIsOpen(index)
    return bool(res)


def udp_remove(index, ip, port):
    index = c_int(index)
    ip = create_string_buffer(ip.encode('gbk'), 30)
    port = c_ushort(port)
    vdm.UdpRemove.restype = c_bool
    res = vdm.UdpRemove(index, ip, port)
    return bool(res)


def udp_send_request_connect(index, ip, port):
    index = c_int(index)
    ip = create_string_buffer(ip.encode('gbk'), 30)
    port = c_ushort(port)
    vdm.UdpSendRequestConnect.restype = c_bool
    res = vdm.UdpSendRequestConnect(index, ip, port)
    sleep(0.1)
    return bool(res)


def udp_recv_mocap_data(index, ip, port, mocap_data):
    index = c_int(index)
    ip = create_string_buffer(ip.encode('gbk'), 30)
    port = c_ushort(port)
    vdm.UdpRecvMocapData.restype = c_bool
    res = vdm.UdpRecvMocapData(index, ip, port, pointer(mocap_data))
    return bool(res)


def udp_get_recv_initial_tpose_position(index, ip, port, ws, body, r_hand, l_hand):
    index = c_int(index)
    ip = create_string_buffer(ip.encode('gbk'), 30)
    port = c_ushort(port)
    ws = c_int(ws)

    type_float_array_3 = c_float * 3
    type_float_array_3_23 = c_float * 3 * 23
    type_float_array_3_20 = c_float * 3 * 20
    c_body = type_float_array_3_23()
    c_rhand = type_float_array_3_20()
    c_lhand = type_float_array_3_20()

    for i in range(23):
        for j in range(len(body[0])):
            c_body[i][j] = c_float(body[i][j])
    for i in range(20):
        for j in range(len(r_hand[0])):
            c_rhand[i][j] = c_float(r_hand[i][j])
            c_lhand[i][j] = c_float(l_hand[i][j])
    vdm.UdpGetRecvInitialTposePosition.restype = c_bool
    res = vdm.UdpGetRecvInitialTposePosition(index, ip, port, ws, c_body, c_rhand, c_lhand)
    sleep(0.1)
    for i in range(len(body)):
        for j in range(len(body[0])):
            body[i][j] = float(body[i][j])
    for i in range(len(r_hand)):
        for j in range(len(r_hand[0])):
            r_hand[i][j] = float(c_rhand[i][j])
            l_hand[i][j] = float(c_lhand[i][j])
    return bool(res)


def read_modal_pose_head():
    init_body_location = [None] * 23
    for i in range(23):
        init_body_location[i] = [0, 0, 0]
    init_rhand_location = [None] * 20
    init_lhand_location = [None] * 20
    for i in range(20):
        init_rhand_location[i] = [0, 0, 0]
        init_lhand_location[i] = [0, 0, 0]
        

    return init_body_location, init_rhand_location, init_lhand_location
