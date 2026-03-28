import time
import collector
from rich.live import Live
from rich.table import Table
from rich.progress import track
import modify_metrics

def make_cpu_cores_table(cpu_percentage_list_per_core):
    core_tbl = Table(box=None)
    for core_percentage in cpu_percentage_list_per_core:
        core_tbl.add_row(core_percentage)
    return core_tbl

def make_cpu_table():
    cpu_tbl = Table("CPU Metric", "CPU Value", title="CPU Monitor", show_lines=True)
    cpu_percentage_list_per_core, cpu_percentage_aggregated = collector.get_cpu_data()
    cpu_tbl.add_row("CPU Usage (aggregated)", cpu_percentage_aggregated)
    core_tbl = make_cpu_cores_table(cpu_percentage_list_per_core)
    cpu_tbl.add_row("CPU Usage (per-core)", core_tbl)
    return cpu_tbl

def make_memory_table():
    memory_tbl = Table("Memory Metric", "Memory Value", title="Memory Monitor", show_lines=True)
    used_memory_bytes, total_memory_bytes, used_memory_percentage = collector.get_memory_data()
    used_memory = modify_metrics.bytes2human(used_memory_bytes)
    total_memory = modify_metrics.bytes2human(total_memory_bytes)
    memory_tbl.add_row("Used Memory", used_memory)
    memory_tbl.add_row("Total Memory", total_memory)
    memory_tbl.add_row("Percentage of Used Memory", used_memory_percentage)
    return memory_tbl

def main():

    with Live(refresh_per_second=1) as live:
        while True:
            grid = Table(box=None, title="[cyan]System Monitor")
            cpu_tbl = make_cpu_table()
            memory_tbl = make_memory_table()
            grid.add_column(cpu_tbl)
            grid.add_column(memory_tbl)
            live.update(grid)
            time.sleep(2)
if __name__ == "__main__":
    main()