import json
from json import JSONDecodeError

logging_format = ""
logging_path = ""
CSV_HEADER_FIELDNAMES = ["time",""]

def prepare_logger(input_format, input_path):
    global logging_format
    logging_format = input_format
    global logging_path
    logging_path = input_path


def log(system_readings):
    if logging_path:
        lst=[]
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
