import socket
import pandas as pd
from time import sleep, time
import function as VDDR
from node_list import BodyNodes
from datetime import datetime, time
def get_current_seconds():
    """
    Funkcja zwracająca liczbę sekund od północy.

    :return: Liczba sekund od północy.
    :rtype: float
    """
    now = datetime.now()
    midnight = datetime.combine(now.date(), time())
    seconds_since_midnight = (now - midnight).total_seconds()
    return seconds_since_midnight


def savetocsv(data, start_seconds):
    """
    Funkcja zapisująca dane z ruchu motion capture (mocap) do pliku CSV.
    :param data: obiekt zawierający dane.
    :param start_seconds: Początkowy czas w sekundach, od którego liczony jest czas w danych mocap.
    """
    mocap_dict = {'time(ms)': [int((get_current_seconds() - start_seconds) * 1000)]}
    for i, node in enumerate(BodyNodes):
        for j in range(3):
            mocap_dict[f'{node} position {["X", "Y", "Z"][j]}(m)'] = [data.position_body[i][j]]
        for k in range(4):
            mocap_dict[f'{node} quaternion {k}'] = [data.quaternion_body[i][k]]

    df = pd.DataFrame(mocap_dict)
    csv_filename = 'bodynodes_data.csv'
    try:
        existing_df = pd.read_csv(csv_filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(csv_filename, index=False)

"""
Kod producenta Virdyn
"""
index = 0
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 7000
tag1 = VDDR.udp_open(index, 0)
print('打开UDP='+str(tag1))
tag1 = VDDR.udp_send_request_connect(index, ip, port) # Połączenie
print('连接='+str(tag1))
"""
Kod producenta Virdyn
"""
start_seconds = get_current_seconds()

"""
Zmodyfikowana pętla for, umożliwiająca zapisywanie zebranych danych do pliku CSV
"""
for i in range(1000):
    sleep(0.001)
    if VDDR.udp_is_open(index):
        mocap_data = VDDR.MocapData()
        VDDR.udp_recv_mocap_data(index, ip, port, mocap_data)
        if mocap_data.isUpdate: 
            savetocsv(mocap_data, start_seconds)

VDDR.udp_close(index)

