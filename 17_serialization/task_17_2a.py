# -*- coding: utf-8 -*-
'''
Задание 17.2a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод команды show cdp neighbor из нескольких файлов и записывает итоговую топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами, независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь в файл topology.yaml.

'''

import yaml
import re


def parse_cdp_neighbors(line: str):
    """ line - result of sh cdp neighbors. return dict"""

    local_device = re.search(r'\w+', line).group()
    table = line[re.search(r'Device', line).span()[0]:]
    table = re.sub(r' {2,}', ',', table)
    table = table.split('\n')
    bigger_dict = dict()
    for item in table[1:]:
        if item:
            final = item.split(',')
            bigger_dict[final[1]] = {final[0]: final[5]}
        else:
            continue
    return {local_device: bigger_dict}


def generate_topology_from_cdp(list_of_files: list, save_to_filename=None):
    main_dictionary = dict()
    for file_name in list_of_files:
        with open(file_name) as file:
            line = file.read()
            ret_value = parse_cdp_neighbors(line)
            main_dictionary.update(ret_value)
    if save_to_filename:
        with open(save_to_filename + '.yaml', 'w') as f:
            yaml.dump(main_dictionary, f)
    print(main_dictionary)


file_list = """* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt"""

file_list = [item for item in file_list.split() if item != '*']
generate_topology_from_cdp(file_list, 'new')
