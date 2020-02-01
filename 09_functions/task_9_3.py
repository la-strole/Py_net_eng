# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


def configure_function(config_file_name):
    """read from conf file
    """
    dict_access = dict()
    dict_trunk = dict()
    conf = (dict_access, dict_trunk)
    with open(config_file_name, 'r') as file:
        lines = file.read().split('\n')
        for line_num in range(len(lines)):
            if 'switchport access vlan' in lines[line_num]:
                dict_access[lines[line_num - 2].split()[1]] = int(lines[line_num].split()[-1])
            elif 'switchport trunk allowed vlan' in lines[line_num]:
                dict_trunk[lines[line_num - 2].split()[1]] = [int(x) for x in lines[line_num].split()[-1].split(',')]
    return conf


print(configure_function('config_sw2.txt'))

