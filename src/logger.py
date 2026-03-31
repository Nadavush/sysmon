import json

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
        with open(logging_path,'a') as input_file:
            json.dump(system_readings, input_file)



