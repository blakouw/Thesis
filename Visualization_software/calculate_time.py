import pandas as pd


def calculate_time(file_path):
    """
    Funkcja oblicza różnicę czasową na podstawie pliku CSV.
    :param: file_path: Ścieżka do pliku CSV zawierającego dane czasowe.
    :return: Różnica czasowa między pierwszym a ostatnim wpisem w pliku.
    """
    data = pd.read_csv(file_path, usecols=[0])
    difference = data.iloc[-1, 0] - data.iloc[0, 0]

    return difference
