# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
from sys import argv

ignore = ['duplex', 'alias', 'Current configuration']
with open('config_sw1.txt', 'r') as conf_file:
    for line in conf_file:
        if not line.startswith('!'):
            for ignore_word in ignore:
                if line.find(ignore_word) == -1:
                    continue
                else:
                    break
            else:
                print(line.strip())
        continue
