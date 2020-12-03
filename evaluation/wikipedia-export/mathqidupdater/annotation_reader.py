import os


def get_file_list(location):
    return [f for f in os.listdir(location) if f.endswith('.csv')]


