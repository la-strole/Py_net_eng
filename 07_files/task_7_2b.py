# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']
with open('config_sw1.txt', 'r') as config_file, open('test_write.txt', 'a') as write_file:
    for line in config_file:
        for word_ignore in ignore:
            if word_ignore in line:
                break
        else:
            write_file.write(line)
