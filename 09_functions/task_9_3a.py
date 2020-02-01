# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
from typing import Dict


def configure_function(config_file_name):
    """read from conf file
    """
    dict_access: Dict[str, int] = dict()
    dict_trunk: Dict = dict()
    int_block = dict()
    with open(config_file_name, 'r') as file:
        while True:
            line = file.readline().strip()
            if line.startswith('interface'):
                interface_name = line.split()[1]
                int_block[interface_name] = []
                line = file.readline().strip()
                while line != '!':
                    int_block[interface_name].append(line)
                    line = file.readline().strip()
            else:
                if line == 'end':
                    break
        for key in int_block.keys():
            key_line = ','.join(int_block[key])
            if 'switchport mode access' in key_line:
                if 'switchport access vlan' in key_line:
                    dict_access[key] = int(int_block[key][1].split()[-1])
                else:
                    dict_access[key] = 1
            elif 'switchport trunk' in key_line:
                if 'switchport trunk allowed vlan' in key_line:
                    dict_trunk[key] = [int(x) for x in int_block[key][1].split()[-1].split(',')]
                else:
                    dict_trunk[key] = 'all'
    return dict_access, dict_trunk


print(configure_function('config_sw1.txt'))
