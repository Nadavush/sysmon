import psutil
import modify_metrics
import os

def get_cpu_data():
    """Gets using psutil API list of percentages per core and aggragated percentage in cpu,
     modifies them to become strings with '%' symbols at the end.
     Args:

     Return value:
        dict{str:list[str],str:str}: A dictionary of a value title and a list of percentages for each CPU core,
        an aggregated percentage of the CPU.
        """
    percentage_list_per_core = psutil.cpu_percent(percpu=True)
    percentage_aggregated = psutil.cpu_percent()
    percentage_list_per_core = modify_metrics.convert_num_list_to_percentage(percentage_list_per_core)
    percentage_aggregated = modify_metrics.convert_num_to_percentage(percentage_aggregated)
    return {"percentage-per-core":percentage_list_per_core, "percentage-aggregated":percentage_aggregated}

def get_memory_data():
    """Gets using psutil API various data on memory, extracts out of it only
    the used memory (converted from bytes), the total memory (converted from bytes),
    and the used percentage (as a percentage) into a tuple of strings.
    Args:

    Return value:
        dict{str:int,str:int,str:str}: A dictionary of a value title and the number in memory of used bytes,
        number of total bytes, percentage of used bytes.
        """
    memory_data = psutil.virtual_memory()
    total_memory = memory_data.total
    used_memory = memory_data.used
    used_memory_percentage = modify_metrics.convert_num_to_percentage(memory_data.percent)
    return {"used":used_memory, "total":total_memory, "used-percentage":used_memory_percentage}

def get_disk_data():
    """Gets using psutil API a list of disk partitions, iterates through them and saves each ones data
    (partition mountpoint, total bytes, used bytes, percentage of used bytes) in a dict.
    Args:

    Return value:
        list[dict{str:str,str:int,str:int,str:str}]:A list of dictionaries, each one holding value names and respective
        values of partition's mountpoint, total bytes, used bytes, used percentage.
    """
    partitions_data_list = []
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or not part.fstype:
                #skip cd-rom drives with no disk, which may raise an error if we don't skip
                continue
        usage = psutil.disk_usage(part.mountpoint)
        total_partition = usage.total
        used_partition = usage.used
        used_partition_percentage = modify_metrics.convert_num_to_percentage(usage.percent)
        partitions_data_list.append({"partition-mountpoint":part.mountpoint,"used":used_partition,"total":total_partition,"used-percentage":used_partition_percentage})
    return partitions_data_list

def get_network_data(interval, prev_bytes_sent=0, prev_bytes_recv=0):
    """Gets using psutil API the number of bytes sent, bytes received, then calculates with args the network upload
    and download speeds, formats the network speeds, returns the respective data in a dict
    Args:
        interval: time between current reading and previous; essential to calculate network speed.
        prev_bytes_sent: bytes sent in last reading; essential to calculate network speed
        prev_bytes_recv: bytes received last reading; essential to calculate network speed

    Return value:
        dict{str:str,str:str,str:int,str:int}: dict of value names corresponding to upload speed (as str), download speed
        (as str), number of bytes sent (as int), number of bytes received (as int)
    """
    network_data = psutil.net_io_counters()
    bytes_sent = network_data.bytes_sent
    bytes_recv = network_data.bytes_recv
    upload_speed = __calculate_network_speed(interval, bytes_sent, prev_bytes_sent)
    upload_speed = modify_metrics.add_mbps_and_format_speed(upload_speed)
    download_speed = __calculate_network_speed(interval, bytes_recv, prev_bytes_recv)
    download_speed = modify_metrics.add_mbps_and_format_speed(download_speed)

    return {"upload-speed":upload_speed,"download-speed":download_speed, "sent":bytes_sent, "received":bytes_recv}

def __calculate_network_speed(interval, curr_bytes, prev_bytes):
    """calculates an upload/download speed in bytes per sec with the formula
    (current bytes - previous bytes) / time passed. then changes speed to mbps.
    Args:
        interval: time passed since previous bytes captured
        curr_bytes: current bytes captured sent/received in network
        prev_bytes: bytes captured sent/received in network x time before current bytes were captured
    Return value:
        float: download/upload speed"""
    speed_in_bytes_per_sec = (curr_bytes-prev_bytes)/interval
    speed_in_mbps = speed_in_bytes_per_sec * 8.0* (10**-6)
    return speed_in_mbps
