import json
from json import JSONDecodeError

logging_path = ""

def prepare_logger(input_path):
    global logging_path
    logging_path = input_path


def log(system_readings):
    if logging_path:
        with open(logging_path,'r') as input_file:
            try:
                curr_data = json.load(input_file)
            except JSONDecodeError:
                curr_data = None
        if type(curr_data) is list:
            curr_data.append(system_readings)
        else:
            curr_data = [system_readings]
        with open(logging_path, 'w') as input_file:
            json.dump(curr_data, input_file)
