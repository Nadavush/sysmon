from time import sleep

import psutil
import os
from psutil._common import bytes2human
def get_cpu_data():
    """"""
    percentage_list_per_core = psutil.cpu_percent(percpu=True)
    percentage_aggragated = psutil.cpu_percent()
    percentage_list_per_core = _convert_num_list_to_percentage(percentage_list_per_core)
    percentage_aggragated = _convert_num_to_percentage(percentage_aggragated)
    return percentage_list_per_core, percentage_aggragated

def get_memory_data():
    """Gets using psutil API various data on memory, extracts out of it only
    the used memory (converted from bytes), the total memory (converted from bytes),
    and the used percentage (as a percentage) into a tuple of strings.
    Args:
    Return value:
        tuple: (str: used memory, str: total memory, str: percentage of used memory)
        """
    memory_data = psutil.virtual_memory()
    total_memory = bytes2human(memory_data.total)
    used_memory = bytes2human(memory_data.used)
    used_memory_percentage = _convert_num_to_percentage(memory_data.percent)
    return used_memory, total_memory, used_memory_percentage

def get_disk_data():
    partitions_data_list = []
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or not part.fstype:
                #skip cd-rom drives with no disk, which may raise an error if we don't skip
                continue
        usage = psutil.disk_usage(part.mountpoint)
        total_partition = bytes2human(usage.total)
        used_partition = bytes2human(usage.used)
        used_partition_percentage = _convert_num_to_percentage(usage.percent)
        partitions_data_list.append((used_partition,total_partition,used_partition_percentage))
    return partitions_data_list

def get_network_data(interval, prev_bytes_sent=0, prev_bytes_recv=0):
    """"""
    network_data = psutil.net_io_counters()
    bytes_sent = network_data.bytes_sent
    bytes_recv = network_data.bytes_recv
    upload_speed = _calculate_network_speed(interval, bytes_sent, prev_bytes_sent)
    upload_speed = _add_mbps_of_measure_to_speed(upload_speed)
    download_speed = _calculate_network_speed(interval, bytes_recv, prev_bytes_recv)
    download_speed = _add_mbps_of_measure_to_speed(download_speed)

    return upload_speed,download_speed, bytes_sent, bytes_recv

def _add_mbps_of_measure_to_speed(speed):
    return str(speed)+" Mbps"
def _calculate_network_speed(interval, curr_bytes, prev_bytes):
    """"""
    speed_in_bytes_per_sec = (curr_bytes-prev_bytes)/interval
    speed_in_mbps = speed_in_bytes_per_sec * 8.0* (10**-6)
    return speed_in_mbps
def _convert_num_to_percentage(percentage_num):
    """gets a value, makes it a string, and adds a '%' symbol at the end.
    wor"""
    if type(percentage_num) == float or type(percentage_num) == int:
        percentage_value = str(percentage_num)
        percentage_value+="%"
        return percentage_value
    return None
def _convert_num_list_to_percentage(num_list):
    percentage_list = []
    for percentage_num in num_list:
        converted_num = _convert_num_to_percentage(percentage_num)
        if converted_num:
            percentage_list.append(converted_num)
    return percentage_list