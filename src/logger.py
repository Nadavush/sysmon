import csv

logging_format = ""
logging_path = ""
CSV_HEADER_FIELDNAMES = ["time",""]

def prepare_logger(input_format, input_path):
    global logging_format
    logging_format = input_format
    global logging_path
    logging_path = input_path


def log(system_readings,time):
    hey = 3

def json_log(system_readings,time):
    hey = 4


def log_csv(system_readings,time):
    with open(logging_path, 'a',newline="") as input_file:

        writer = csv.writer(input_file)

