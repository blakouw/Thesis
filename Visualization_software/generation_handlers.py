import numpy as np


def print_key(n):
    """
    Funkcja print_key generuje i wypisuje sformatowany klucz składający się z n liczb równo rozmieszczonych
    w zakresie od 0 do 1.
    :param n: Liczba określająca ilość elementów w kluczu.
    :return: Sformatowany klucz w postaci tekstu.
    """
    numbers = np.linspace(0, 1, n)

    formatted_numbers = 'key[' + ', '.join(map(str, numbers)) + ']'
    print(formatted_numbers)

    return formatted_numbers


def convert_to_comma_separated_string(numbers):
    """
    Funkcja zamieniająca listę liczb na ciąg znaków, gdzie liczby są oddzielone przecinkami.
    :param numbers: Lista liczb do przekształcenia.
    :return: Ciąg znaków zawierający liczby oddzielone przecinkami.
    """
    return ','.join(map(str, numbers))


def format_midpoints(label):
    """
    Funkcja formatująca punkty środkowe.
    :param label: Słownik zawierający etykietę, w tym listę punktów środkowych.
    :return: Sformatowane punkty środkowe jako ciąg znaków.
    :raises ValueError: Jeśli 'midpoints' nie jest obecne w etykiecie lub nie jest listą.
    """
    if 'midpoints' not in label or not isinstance(label['midpoints'], list):
        return "ERR nie ma na liscie/midpoints"

    formatted_midpoints = ['{:.4f} {:.4f} {:.4f}'.format(*midpoint) for midpoint in label['midpoints']]

    return ', '.join(formatted_midpoints)


def format_euler(label):
    """
    Funkcja formatująca kąty Eulera zawarte w etykiecie.
    :param label: Słownik zawierający etykietę, w tym listę kątów eulera.
    :return: Sformatowane kąty eulera jako ciąg znaków.
    :raises ValueError: Jeśli 'euler_angles' nie jest obecne w etykiecie lub nie jest listą.
    """
    if 'euler_angles' not in label or not isinstance(label['euler_angles'], list):
        return "ERR nie ma na liscie/euler"

    formatted_midpoints = ['{:.4f} {:.4f} {:.4f} {:.4f}'.format(*midpoint) for midpoint in label['euler_angles']]

    return ', '.join(formatted_midpoints)
