import psutil
import modify_metrics
import os

def get_cpu_data():
    """Gets using psutil API list of percentages per core and aggragated percentage in cpu,
     modifies them to become strings with '%' symbols at the end.
     Args:
     Return value:
        tuple: (list: str: percentage per core, str: aggregated percentage)
        """
    percentage_list_per_core = psutil.cpu_percent(percpu=True)
    percentage_aggregated = psutil.cpu_percent()
    percentage_list_per_core = modify_metrics.convert_num_list_to_percentage(percentage_list_per_core)
    percentage_aggregated = modify_metrics.convert_num_to_percentage(percentage_aggregated)
    return {"percentages-per-core":percentage_list_per_core, "percentage-aggregated":percentage_aggregated}

def get_memory_data():
    """Gets using psutil API various data on memory, extracts out of it only
    the used memory (converted from bytes), the total memory (converted from bytes),
    and the used percentage (as a percentage) into a tuple of strings.
    Args:
    Return value:
        tuple: (str: used memory, str: total memory, str: percentage of used memory)
        """
    memory_data = psutil.virtual_memory()
    total_memory = memory_data.total
    used_memory = memory_data.used
    used_memory_percentage = modify_metrics.convert_num_to_percentage(memory_data.percent)
    return {"used":used_memory, "total":total_memory, "used-percentage":used_memory_percentage}

def get_disk_data():
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
    """"""
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
