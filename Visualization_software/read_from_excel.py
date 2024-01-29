import pandas as pd
from Visualization_software.const import file_path_csv


def extract_data():
    """
    Funkcja do ekstrakcji danych z pliku CSV zawierającego informacje o pozycji i kwaternionach.
    :return: Krotka zawierająca dwie struktury danych:
    - extracted_data: Słownik zawierający dane pozycji i kwaternionów pogrupowane według węzłów.
    - position_data: Słownik zawierający dane pozycji pogrupowane według osi X, Y, Z i węzłów.
    """
    data = pd.read_csv(file_path_csv)

    position_columns = [col for col in data.columns if 'position' in col]
    quaternion_columns = [col for col in data.columns if 'quaternion' in col]

    extracted_data = {}

    for col in position_columns + quaternion_columns:
        node_name = col.split(' ')[0]

        if node_name not in extracted_data:
            extracted_data[node_name] = {'position': [], 'quaternion': []}

        if 'position' in col:
            extracted_data[node_name]['position'].append(data[col].tolist())
        elif 'quaternion' in col:
            extracted_data[node_name]['quaternion'].append(data[col].tolist())

    for node in extracted_data:
        extracted_data[node]['position'] = list(zip(*extracted_data[node]['position']))
        extracted_data[node]['quaternion'] = list(zip(*extracted_data[node]['quaternion']))

    position_data = {}
    for col in position_columns:
        node_name = col.split(' ')[0]
        axis = col.split(' ')[2][0]
        if node_name not in position_data:
            position_data[node_name] = {'X': [], 'Y': [], 'Z': []}
        position_data[node_name][axis].append(data[col][0])

    for node in position_data:
        position_data[node] = list(zip(position_data[node]['X'], position_data[node]['Y'], position_data[node]['Z']))[0]
    global data_len
    data_len = len(data)
    return extracted_data, position_data
data_len = 0

a,b = extract_data()
