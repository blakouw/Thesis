import pandas as pd


def normalize_motion_capture_data_lokal(file_path, output_file='../Input_csv/linia_prosta_norm_lokal.csv', reference_point_xy='Hips',
                                        refrence_point_z='LeftToe'):
    """
    Normalizuje dane z ruchu przechwyconego z kamery, dostosowując pozycję do lokalnego układu współrzędnych.
    :param file_path: Ścieżka do pliku CSV zawierającego dane ruchu przechwycone z kamery.
    :param output_file: Ścieżka do pliku CSV, w którym zostaną zapisane znormalizowane dane. Domyślnie '../Input_csv/linia_prosta_norm_lokal.csv'.
    :param reference_point_xy: Nazwa punktu referencyjnego dla osi XY. Domyślnie 'Hips'.
    :param refrence_point_z: Nazwa punktu referencyjnego dla osi Z. Domyślnie 'LeftToe'.
    :return: Brak zwracanej wartości. Znormalizowane dane zostaną zapisane do podanego pliku CSV.
    """
    data = pd.read_csv(file_path)
    offset_x = -data[reference_point_xy + ' position X(m)'].iloc[0]
    offset_y = -data[reference_point_xy + ' position Y(m)'].iloc[0]
    offset_z = max(-data[refrence_point_z + ' position Z(m)'].iloc[0], 0)

    position_columns = [col for col in data.columns if 'position' in col]
    for col in position_columns:
        if ' X(m)' in col:
            data[col] += offset_x
        elif ' Y(m)' in col:
            data[col] += offset_y
        elif ' Z(m)' in col:
            data[col] += offset_z

    data.to_csv(output_file, index=False)

def normalize_motion_capture_data_global(file_path, output_file='../Input_csv/linia_prosta_norm_global.csv',
                                         reference_point_xy='Hips', reference_point_z='LeftToe'):
    """
    Normalizuje dane z ruchu przechwyconego z kamery, dostosowując pozycję do globalnego układu współrzędnych.
    :param file_path: Ścieżka do pliku CSV zawierającego dane ruchu przechwycone z kamery.
    :param output_file: Ścieżka do pliku CSV, w którym zostaną zapisane znormalizowane dane. Domyślnie '../Input_csv/linia_prosta_norm_lokal.csv'.
    :param reference_point_xy: Nazwa punktu referencyjnego dla osi XY. Domyślnie 'Hips'.
    :param refrence_point_z: Nazwa punktu referencyjnego dla osi Z. Domyślnie 'LeftToe'.
    :return: Brak zwracanej wartości. Znormalizowane dane zostaną zapisane do podanego pliku CSV.
    """
    data = pd.read_csv(file_path)
    position_columns = [col for col in data.columns if 'position' in col]

    for index, row in data.iterrows():
        offset_x = -row[reference_point_xy + ' position X(m)']
        offset_y = -row[reference_point_xy + ' position Y(m)']
        offset_z = max(-row[reference_point_z + ' position Z(m)'], 0)

        for col in position_columns:
            if ' X(m)' in col:
                data.at[index, col] += offset_x
            elif ' Y(m)' in col:
                data.at[index, col] += offset_y
            elif ' Z(m)' in col:
                data.at[index, col] += offset_z

    data.to_csv(output_file, index=False)


normalize_motion_capture_data_lokal('../Input_csv/liniaprosta.csv')
normalize_motion_capture_data_global('../Input_csv/liniaprosta.csv')


