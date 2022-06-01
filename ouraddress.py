from multiprocessing import Process
from numpy import array_split
from json import load
from os import listdir, getenv, makedirs
from os.path import exists as file_exists
from os.path import join as join_path
from os import remove as remove_file
from thefuzz import fuzz
from thefuzz import process
from datetime import datetime
from utils import *

class Ouraddress:

    def __init__(self):

        self.config_parameters = read_json_file("config.json", encoding='latin-1')

        create_path_if_not_exists(self.config_parameters["input folder"])
        create_path_if_not_exists(self.config_parameters["output folder"])
        create_path_if_not_exists(self.config_parameters["temp folder"])

        self.instances = self.config_parameters["instances"]

        print_log(f"Loaded configuration: {self.config_parameters}")

    def prepare_input_data(self, street, ine_code, delimeter, encoding='latin-1'):

        input_file = join_path(self.config_parameters["input folder"], listdir(self.config_parameters["input folder"])[0])

        print_log(f"Iniciando comprobacion de integridad del archivo {input_file}")

        headers = get_headers(input_file, delimeter, encoding=encoding)

        print_log(f"Cabecera detectada {headers}")

        if not check_csv_integrity(input_file, delimeter, encoding='latin-1'):

            print_log(f"Problemas de integridad detectados")

            fix_csv_integrity(input_file, delimeter, encoding='latin-1')

            print_log(f"Problemas de integridad solucionados")
        
        index_ine_code = headers.index(ine_code)
        index_street = headers.index(street)

        print_log(f"Cambiando el orden de las columnas")

        if index_ine_code != 0:
            
            print_log(f"Cambiando columnas de codigo municipal")

            change_csv_columns(input_file, 0, index_ine_code, delimeter, encoding='latin-1')

            headers = get_headers(input_file, delimeter, encoding=encoding)

            index_street = headers.index(street)
        
        if index_street != 1:

            print_log(f"Cambiando columnas de calles")

            change_csv_columns(input_file, 1, index_street, delimeter, encoding='latin-1')
        
        headers = get_headers(input_file, delimeter, encoding=encoding)

        print_log(f"Cabeceras finales {headers}")

        print_log(f"Normalizando delimitadores")

        replace_text_file(input_file, delimeter, "#", encoding='latin-1')

        print_log(f"Input normalizado")
        
    def split_input_file(self):

        print_log(f"Dividiendo input en " + self.config_parameters["temp folder"])

        input_file = join_path(self.config_parameters["input folder"], listdir(self.config_parameters["input folder"])[0])

        input_file_data = read_file(input_file, encoding='latin-1')

        headers = input_file_data[0]

        clean_dir(self.config_parameters["temp folder"])
        
        for line in input_file_data[1:]:

            temp_path = join_path(self.config_parameters["temp folder"], line.split("#")[0])

            if not file_exists(temp_path):

                write_file(temp_path, headers, encoding='latin-1', jump_line=False)              
            
            write_file(temp_path, line, encoding='latin-1', jump_line=False)

        print_log(f"Division de input finalizada")

        print_log(f"Limpiando directorio " + self.config_parameters["input folder"])

        clean_dir(self.config_parameters["input folder"])

    def file_search_fuzzy(self, id):

        search_data_path =  join_path(self.config_parameters["search folder"], id)
        input_data_path = join_path(self.config_parameters["temp folder"], id)
        output_data_path = join_path(self.config_parameters["output folder"], id)

        search_data = read_file(search_data_path, encoding='latin-1')
        input_data = read_file(input_data_path, encoding='latin-1')

        data_headers = get_headers(input_data_path, "#", encoding='latin-1')
        search_headers = get_headers(search_data_path, "#", encoding='latin-1')

        remove_file(input_data_path)

        data_headers = "#".join(data_headers)
        search_headers = "#".join(search_headers)

        write_file(output_data_path, f"{data_headers}#{search_headers}#score", encoding='latin-1', jump_line=True)

        # HASTA AQUI TODO BIEN

        for data in input_data[1:]:

            data = data.strip()

            data_address = data.split("#")[1]
            best_address_data, score_adress = "", 0

            for search in search_data:

                search = search.strip()
                search_address = search.split("#")[0]

                score = fuzz.token_sort_ratio(data_address, search_address)

                if score > score_adress:
                    best_address_data, score_adress = search, score, 
                
                if score_adress >= self.config_parameters["early stop"]:
                    break

            if score_adress >= self.config_parameters["min match valid"]:

                with open(output_data_path, "a", encoding='latin-1') as f:
                    data = data.strip()
                    f.write(f"{data}#{best_address_data}#{score_adress}\n")

    def file_search_fuzzy_multiprocessing(self, temp_files, index):

        print_log(f"Thread {index} entry [file_search_fuzzy_multiprocessing] {temp_files}")
        
        for file in temp_files:

            print_log(f" Thread {index} file {file} started")

            start = datetime.now()

            self.file_search_fuzzy(file)

            end = datetime.now()
            
            print_log(f" Thread {index} file {file} ended [" + str(end-start) + "]")

    def file_search_fuzzy_multiprocessing_init(self):

        self.split_input_file()

        temp_files = listdir(self.config_parameters["temp folder"])

        temp_files_splits = array_split(temp_files, self.instances)

        print_log(f"Files splited distribution: [{temp_files_splits}]")

        threads = []

        for index in range(len(temp_files_splits)):

            temp_files_thread = temp_files_splits[index]

            if len(temp_files_thread) != 0:

                print_log(f"Thread {index} call with parameters: {temp_files_thread}")

                x = Process(target=self.file_search_fuzzy_multiprocessing, args=(temp_files_thread, index, ))

                threads.append(x)

                x.start()

        start = datetime.now()

        for index, thread in enumerate(threads):
            thread.join()

        end = datetime.now()

        print(datetime.now().strftime("%D %H:%M:%S"), " Total time used in threads calculations: ", end-start)

        start = datetime.now()

        print(datetime.now().strftime("%D %H:%M:%S"), " Output join started")

        output_files = listdir(self.config_parameters["output folder"])

        for output_file in output_files:

            with open(join_path(self.config_parameters["output folder"], output_file), "r", encoding='latin-1') as f:
                data = f.readlines()         

            if not file_exists(join_path(self.config_parameters["output folder"], "ouradress.csv")):

                with open(join_path(self.config_parameters["output folder"], "ouradress.csv"), "w", encoding='latin-1') as f:

                    for line in data:

                        if line != "\n":

                            f.write(line)
            
            else:

                with open(join_path(self.config_parameters["output folder"], "ouradress.csv"), "a", encoding='latin-1') as f:

                    for line in data[1:]:

                        if line != "\n":

                            f.write(line)
            
            if ".csv" not in output_file:
            
                remove_file(join_path(self.config_parameters["output folder"], output_file))

        end = datetime.now()

        print(datetime.now().strftime("%D %H:%M:%S"), " Output join ended [", end-start, "]")

        output_file_end = join_path(self.config_parameters["output folder"], "ouradress.csv")

        print(datetime.now().strftime("%D %H:%M:%S"), f" Output file: {output_file_end}")    