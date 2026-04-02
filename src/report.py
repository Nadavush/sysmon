import json

def parse_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
