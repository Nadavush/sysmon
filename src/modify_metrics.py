from psutil._common import bytes2human


def convert_num_to_percentage(percentage_num):
    """gets a value, makes it a string, and adds a '%' symbol at the end.
    wor"""
    if type(percentage_num) == float or type(percentage_num) == int:
        percentage_value = str(percentage_num)
        percentage_value+="%"
        return percentage_value
    return None
def convert_num_list_to_percentage(num_list):
    percentage_list = []
    for percentage_num in num_list:
        converted_num = convert_num_to_percentage(percentage_num)
        if converted_num:
            percentage_list.append(converted_num)
    return percentage_list
def add_mbps_of_measure_to_speed(speed):
    return str(speed)+" Mbps"
