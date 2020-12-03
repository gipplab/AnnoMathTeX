import os


def get_file_list(dir):
    return [f for f in os.listdir(dir) if f.endswith('.csv')]

