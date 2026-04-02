import json
import modify_metrics
def generate_report_data(file_path, date):
    with open(file_path, 'r') as file:
        data = json.load(file)
    report_readings_lst = get_all_date_readings(data, date)
    if report_readings_lst:
        used_cpu_lst = []
        used_mem_lst = []
        for reading in report_readings_lst:
            used_cpu_lst.append(modify_metrics.convert_percentage_to_num(reading["cpu"]["percentage-aggregated"]))
            used_mem_lst.append(reading["memory"]["used"])

        highest_cpu_percentage, lowest_cpu_percentage, avg_cpu_percentage = get_highest_lowest_avg(used_cpu_lst)
        highest_used_mem, lowest_used_mem, avg_used_mem = get_highest_lowest_avg(used_mem_lst)
        return {"highest-cpu":highest_cpu_percentage, "lowest-cpu":lowest_cpu_percentage,"avg-cpu":avg_cpu_percentage,
            "highest-mem":highest_used_mem,"lowest-mem":lowest_used_mem,"avg-mem":avg_used_mem}
    else:
        return {}


def get_highest_lowest_avg(lst):
    lst.sort()
    return lst[0], lst[-1], sum(lst)/len(lst)

def get_all_date_readings(data, date):
    filtered_lst = []
    for reading in data:
        if reading["time"][:10]==date:
            filtered_lst.append(reading)
    return filtered_lst