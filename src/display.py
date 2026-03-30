import time
import main
from rich.live import Live
from rich.table import Table
import modify_metrics
import color_values
REFRESH_PER_SECOND = 2
CPU_READINGS_INDEX = 0
MEMORY_READINGS_INDEX = 1
DISK_READINGS_INDEX = 2
NETWORK_READINGS_INDEX = 3

def make_cpu_cores_table(cpu_percentage_list_per_core):
    core_tbl = Table(box=None)
    for core_percentage in cpu_percentage_list_per_core:
        core_percentage = color_values.color_percentage(core_percentage)
        core_tbl.add_row(core_percentage)
    return core_tbl

def make_cpu_table(cpu_readings):
    cpu_tbl = Table("CPU Metric", "CPU Value", title="CPU Monitor", show_lines=True)
    cpu_percentage_list_per_core = cpu_readings["percentage-per-core"]
    cpu_percentage_aggregated = cpu_readings["percentage-aggregated"]
    cpu_percentage_aggregated = color_values.color_percentage(cpu_percentage_aggregated)
    cpu_tbl.add_row("CPU Usage (aggregated)", cpu_percentage_aggregated)
    core_tbl = make_cpu_cores_table(cpu_percentage_list_per_core)
    cpu_tbl.add_row("CPU Usage (per-core)", core_tbl)
    return cpu_tbl

def make_memory_table(memory_readings):
    memory_tbl = Table("Memory Metric", "Memory Value", title="Memory Monitor", show_lines=True)
    used_memory_bytes = memory_readings["used"]
    total_memory_bytes = memory_readings["total"]
    used_memory_percentage = memory_readings["used-percentage"]
    used_memory_percentage = color_values.color_percentage(used_memory_percentage)
    used_memory = modify_metrics.bytes2human(used_memory_bytes)
    total_memory = modify_metrics.bytes2human(total_memory_bytes)
    memory_tbl.add_row("Used Memory", used_memory)
    memory_tbl.add_row("Total Memory", total_memory)
    memory_tbl.add_row("Percentage of Used Memory", used_memory_percentage)
    return memory_tbl

def make_disk_table(disk_readings):
    disk_tbl = Table(title="Disk Monitor", show_header=False, show_edge=True, show_lines=False)
    partitions_data_list = disk_readings
    for part in partitions_data_list:
        partition_mountpoint, used_partition_bytes, total_partition_bytes, used_partition_percentage = part
        used_partition_percentage = color_values.color_percentage(used_partition_percentage)
        used_partition = modify_metrics.bytes2human(used_partition_bytes)
        total_partition = modify_metrics.bytes2human(total_partition_bytes)
        part_tbl = Table(partition_mountpoint+" Metric", partition_mountpoint+" Value", show_lines=True)
        part_tbl.add_row("Used Partition",used_partition)
        part_tbl.add_row("Total Partition", total_partition)
        part_tbl.add_row("Percentage of Used Partition", used_partition_percentage)
        disk_tbl.add_row(part_tbl)
    return disk_tbl

def make_network_table(first_time_flag, network_readings):
    network_tbl = Table("Network Metric","Network Value",title="Network Monitor",show_lines=True)
    if first_time_flag:
        bytes_sent, bytes_recv = network_readings[2:]
        upload_speed = "TBD"
        download_speed = "TBD"
    else:
        upload_speed, download_speed, bytes_sent, bytes_recv = network_readings
    network_tbl.add_row("Upload Speed", upload_speed)
    network_tbl.add_row("Download Speed", download_speed)
    network_tbl.add_row("Data Sent in Bytes", str(bytes_sent))
    network_tbl.add_row("Data Received in Bytes", str(bytes_recv))
    return network_tbl,bytes_sent, bytes_recv, False



def display_monitor(interval):

    with (Live(refresh_per_second=REFRESH_PER_SECOND) as live):
        first_time_flag= True
        prev_network_bytes_sent = 0
        prev_network_bytes_recv = 0
        while True:
            grid = Table(box=None, title="[cyan]System Monitor")
            system_readings = main.get_sys_readings(prev_network_bytes_sent, prev_network_bytes_recv, interval)
            cpu_tbl = make_cpu_table(system_readings["cpu"])
            memory_tbl = make_memory_table(system_readings["memory"])
            disk_tbl = make_disk_table(system_readings["disk"])
            network_tbl, prev_network_bytes_sent, prev_network_bytes_recv, first_time_flag= make_network_table(first_time_flag,system_readings["network"])
            grid.add_row(cpu_tbl,disk_tbl)
            grid.add_row(memory_tbl,network_tbl)
            live.update(grid)
            time.sleep(interval)
