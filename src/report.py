import json

def generate_report(file_path):
    with open(file_path, 'r') as file:
            data = json.load(file)