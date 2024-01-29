import numpy as np

from Visualization_software.calculate_limb_lenghts import updated_limb_pairs
from read_from_excel import extract_data


def calculate_quaternion(P1, P2):
    """
    Funkcja obliczająca kwaternion na podstawie dwóch punktów w przestrzeni.
    :param P1: Pierwszy punkt w formacie [x, y, z].
    :param P2: Drugi punkt w formacie [x, y, z].
    :return: krotka (Qx, Qy, Qz, Qw) reprezentujący kwaternion.
    """
    D = np.array(P2) - np.array(P1)
    D_normalized = D / np.linalg.norm(D)
    y_axis = np.array([0, 1, 0])
    axis = np.cross(y_axis, D_normalized)
    angle = np.arccos(np.dot(D_normalized, y_axis))

    Qx = axis[0] * np.sin(angle / 2) * 2
    Qy = axis[1] * np.sin(angle / 2) * 2
    Qz = axis[2] * np.sin(angle / 2) * 2
    Qw = np.cos(angle / 2) * 2

    return Qx, Qy, Qz, Qw


def calculate_midpoints_and_quaternions_over_time(data, limb_pairs):
    """
    Oblicza środki i kąty Eulera dla kończyn w czasie.
    :param data: Słownik danych zawierający pozycje i kwaterniony w czasie.
    :param limb_pairs: Pary kończyn do przetwarzania.
    :return: Słownik zawierający środki i kąty Eulera dla kończyn w czasie.
    """
    results = {limb: {'midpoints': [], 'euler_angles': []} for limb in limb_pairs}

    for limb in limb_pairs:
        node1, node2 = limb
        if node1 in data and node2 in data:
            for pos1, pos2, quat1, quat2 in zip(data[node1]['position'], data[node2]['position'],
                                                data[node1]['quaternion'], data[node2]['quaternion']):

                midpoint = tuple((np.array(pos1) + np.array(pos2)) / 2)
                results[limb]['midpoints'].append(midpoint)

                avg_quat = tuple((np.array(calculate_quaternion(pos1, pos2))))
                results[limb]['euler_angles'].append(avg_quat)
        else:
            results[limb] = "Node data not available"

    return results


extracted_data, co = extract_data()
limb_midpoints_quaternions = calculate_midpoints_and_quaternions_over_time(extracted_data, updated_limb_pairs)
var = {key: limb_midpoints_quaternions[key] for key in list(limb_midpoints_quaternions.keys())[:2]}
