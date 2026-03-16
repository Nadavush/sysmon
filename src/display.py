import time
import collector
from rich.live import Live
from rich.table import Table

def make_core_table(cpu_percentage_list_per_core):
    core_tbl = Table(box=None)
    for core_percentage in cpu_percentage_list_per_core:
        core_tbl.add_row(core_percentage)
    return core_tbl

def make_cpu_table():
    cpu_tbl = Table("Metric", "Value", title="System Monitor", show_lines=True)
    cpu_percentage_list_per_core, cpu_percentage_aggregated = collector.get_cpu_data()
    cpu_tbl.add_row("CPU Usage (aggregated)", cpu_percentage_aggregated)
    core_tbl = make_core_table(cpu_percentage_list_per_core)
    cpu_tbl.add_row("CPU Usage (per-core)", core_tbl)
    return cpu_tbl

def main():
    with Live(refresh_per_second=1) as live:
        while True:
            grid = Table.grid(expand=True)
            cpu_tbl = make_cpu_table()
            live.update(cpu_tbl)
            time.sleep(2)
if __name__ == "__main__":
    main()