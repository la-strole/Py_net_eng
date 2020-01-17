# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'
list_ospf = ospf_route.replace(',', ' ').split()

print(f'''
{'Protocol:':23} {'OSPF':15}
{'Prefix:':23} {list_ospf[1]:15}
{'AD/Metric:':23} {list_ospf[2][1:-1]:15}
{'Next-Hop: ':23} {list_ospf[4]:15}
{'Last update:':23} {list_ospf[5]:15}
{"Outbound Interface:" :23} {list_ospf[6]:15}
''')
