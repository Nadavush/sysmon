from psutil._common import bytes2human


def convert_num_to_percentage(percentage_num):
    """Converts a num to str and adds to it % symbol at the end
    Args:
        percentage_num: number being converted to str and added % at the end
    Return value:
        str(percentage_num+%)"""
    percentage_value = str(percentage_num)
    percentage_value+="%"
    return percentage_value
def convert_percentage_to_num(percentage):
    """Converts a string of a num with a percentage in the end to a float without the % symbol
    Args:
        percentage: str of a num with a % at the end
    Return value:
        float"""
    return float(percentage.strip("%"))
def convert_num_list_to_percentage(num_list):
    """Converts a list of nums each one to str and adds to each % at the end with convert_num_to_percentage() foreach item
    in list
    Args:
        num_list: list of nums (ints or floats)
    Return value:
        lst[str]"""
    percentage_list = []
    for percentage_num in num_list:
        converted_num = convert_num_to_percentage(percentage_num)
        percentage_list.append(converted_num)
    return percentage_list
def add_mbps_and_format_speed(value):
    """Formats float to have only 2 digits after . and adds to the formatted string Mbps
    Args:
        value: float
    Return value:
        str"""
    formatted_value = "{:.2f}".format(value)
    return formatted_value + " Mbps"