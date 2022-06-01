from json import load
from os import listdir, getenv, makedirs
from os.path import exists as file_exists
from os.path import join as join_path
from os import remove as remove_file
from datetime import datetime 
from copy import deepcopy
from glob import glob

def clean_dir(path):

    files = glob(join_path(path, "*"))

    for f in files:
        remove_file(f)

def create_path_if_not_exists(path):

    if not file_exists(path):
        makedirs(path)

def read_file(path, encoding='latin-1'):

    with open(path, "r", encoding=encoding) as f:
        input_file_data = f.readlines()
    
    return input_file_data

def read_json_file(path, encoding='latin-1'):

    with open(path, "r", encoding=encoding) as f:
        input_file_data = load(f)
    
    return input_file_data

def write_file(path, text, encoding='latin-1', jump_line=True):

    with open(path, "a", encoding=encoding) as f:
        if jump_line:
            f.write(text + "\n")
        else:
            f.write(text)

def print_log(text):

    print(datetime.now().strftime("%D %H:%M:%S"), text)

def split_line(text, delimeter):

    return text.strip().split(delimeter)

def get_headers(path, delimeter, encoding='latin-1'):

    with open(path, "r", encoding=encoding) as f:
        return split_line(read_file(path, encoding=encoding)[0], delimeter)

def check_csv_integrity(path, delimeter, encoding='latin-1'):

    headers = get_headers(path, delimeter, encoding=encoding)
    num_cols = len(headers)

    data = read_file(path)

    for line in data[1:]:

        if len(split_line(line, delimeter)) != num_cols:

            return False
    
    return True

def fix_csv_integrity(path, delimeter, encoding='latin-1'):

    headers = get_headers(path, delimeter, encoding=encoding)
    num_cols = len(headers)

    data = read_file(path)
    data_copy = deepcopy(data)

    for line in data[1:]:

        if len(split_line(line, delimeter)) != num_cols:

            data_copy.remove(line)
    
    remove_file(path)

    for line in data_copy:

        write_file(path, line, encoding='latin-1', jump_line=False)

def change_elements(data, col_1, col_2):

    temp = data[col_1]
    data[col_1] = data[col_2]
    data[col_2] = temp

    return data

def change_csv_columns(path, col_1, col_2, delimeter, encoding='latin-1'):

    data = []

    for line in read_file(path, encoding=encoding):

        temp = split_line(line, delimeter)
        temp = change_elements(temp, col_1, col_2)

        data.append(f"{delimeter}".join(temp))
    
    remove_file(path)

    for line in data:

        write_file(path, line, encoding=encoding, jump_line=True)

def replace_text_file(path, search, replace, encoding='latin-1'):

    data = []

    for line in read_file(path, encoding=encoding):

        data.append(line.replace(search, replace))

    remove_file(path)
    
    for line in data:

        write_file(path, line, encoding=encoding, jump_line=False)
