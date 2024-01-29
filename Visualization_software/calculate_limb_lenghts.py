import numpy as np
from read_from_excel import extract_data

updated_limb_pairs = [
    ('Hips', 'Spine'), ('Spine', 'Spine1'), ('Spine1', 'Spine2'), ('Spine2', 'Spine3'),
    ('Spine3', 'Neck'), ('Neck', 'Head'),
    ('Spine3', 'LeftShoulder'), ('LeftShoulder', 'LeftUpperArm'), ('LeftUpperArm', 'LeftLowerArm'),
    ('LeftLowerArm', 'LeftHand'),
    ('Spine3', 'RightShoulder'), ('RightShoulder', 'RightUpperArm'), ('RightUpperArm', 'RightLowerArm'),
    ('RightLowerArm', 'RightHand'),
    ('Hips', 'LeftUpperLeg'), ('LeftUpperLeg', 'LeftLowerLeg'), ('LeftLowerLeg', 'LeftFoot'), ('LeftFoot', 'LeftToe'),
    ('Hips', 'RightUpperLeg'), ('RightUpperLeg', 'RightLowerLeg'), ('RightLowerLeg', 'RightFoot'),
    ('RightFoot', 'RightToe')
]


def calculate_limb_lengths_from_file(limb_pairs):
    """
    Funkcja oblicza długości kończyn na podstawie danych z pliku.
    :param: limb_pairs: Pary węzłów kończyn w formie listy krotek.
    :return: Słownik zawierający długości kończyn.
    """
    extracted_data, position_data = extract_data()
    limb_lengths = {}
    for limb in limb_pairs:
        node1, node2 = limb
        if node1 in position_data and node2 in position_data:
            distance = np.linalg.norm(np.array(position_data[node1]) - np.array(position_data[node2]))
            limb_lengths[f"('{node1}', '{node2}')"] = distance
        else:
            limb_lengths[f"('{node1}', '{node2}')"] = "Node data not available"

    return limb_lengths

limb_lengths_new = calculate_limb_lengths_from_file(updated_limb_pairs)
print(limb_lengths_new)
