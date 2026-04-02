from psutil._common import bytes2human


def convert_num_to_percentage(percentage_num):
    """converts a value to str and adds to it % symbol at the end"""
    if type(percentage_num) == float or type(percentage_num) == int:
        percentage_value = str(percentage_num)
        percentage_value+="%"
        return percentage_value
    return None
def convert_percentage_to_num(percentage):
    return float(percentage.strip("%"))
def convert_num_list_to_percentage(num_list):
    percentage_list = []
    for percentage_num in num_list:
        converted_num = convert_num_to_percentage(percentage_num)
        if converted_num:
            percentage_list.append(converted_num)
    return percentage_list
def add_mbps_and_format_speed(value):
    formatted_value = "{:.2f}".format(value)
    return formatted_value + " Mbps"
def remove_mbps(value):
    return float(value.strip(" Mbps"))