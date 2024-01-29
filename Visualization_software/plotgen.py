import pandas as pd
import matplotlib.pyplot as plt
from Visualization_software.const import file_path_csv, file_path_csv_normlokal

def plot_node_position(file_path1, file_path2, node, position):
    """
    Tworzy porównawczy wykres pozycji określonego węzła (X, Y lub Z) z dwóch plików CSV.
    :param file_path1: Ścieżka do pierwszego pliku CSV.
    :param file_path2: Ścieżka do drugiego pliku CSV.
    :param node: Nazwa węzła (np. 'LeftUpperLeg').
    :param position:  Pozycja do wyświetlenia ('X', 'Y' lub 'Z').
    """
    column_name = f'{node} position {position}(m)'
    data1 = pd.read_csv(file_path1, usecols=[column_name])
    data2 = pd.read_csv(file_path2, usecols=[column_name])
    plt.figure(figsize=(12, 6))
    plt.plot(data1, color='red', label=f'{file_path1} - {position} Position')
    plt.plot(data2, color='blue', label=f'{file_path2} - {position} Position')
    plt.title(f'Comparison of {node} position {position}(m)')
    plt.xlabel('Time [ms]')
    plt.ylabel(f'{node} position {position}(m)')
    plt.legend()
    plt.show()
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(data1, color='red')
    plt.title(f'{file_path1} - {position} Position')
    plt.xlabel('Time [ms]')
    plt.ylabel(f'{node} position {position}(m)')
    plt.subplot(1, 2, 2)
    plt.plot(data2, color='blue')
    plt.title(f'{file_path2} - {position} Position')
    plt.xlabel('Time [ms]')
    plt.ylabel(f'{node} position {position}(m)')

    plt.tight_layout()
    plt.show()

file_path1 = file_path_csv
file_path2 = file_path_csv_normlokal
node = 'LeftUpperLeg'
position = 'Y'

#plot_node_position(file_path1, file_path2, node, position)

def plot_all_positions(file_path, node):
    """
    Wyświetla wykresy pozycji X, Y i Z określonego węzła z pliku CSV.
    :param file_path: Ścieżka do pliku CSV.
    :param node: Nazwa węzła (np. 'RightUpperLeg').
    """
    column_names = [f'{node} position {pos}(m)' for pos in ['X', 'Y', 'Z']]
    data = pd.read_csv(file_path, usecols=column_names)
    data = data.iloc[360:428]
    plt.figure(figsize=(18, 6))
    for i, pos in enumerate(['X', 'Y', 'Z']):
        plt.subplot(1, 3, i+1)
        plt.plot(data[column_names[i]], label=f'{node} position {pos}')
        plt.title(f'{node} position {pos}')
        plt.xlabel('Time [ms]')
        plt.ylabel(f'Position {pos}(m)')
        plt.legend()

    plt.tight_layout()
    plt.show()

file_path = file_path_csv
node = 'LeftUpperLeg'
plot_all_positions(file_path, node)

