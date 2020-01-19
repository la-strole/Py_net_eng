# -*- coding: utf-8 -*-
'''
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
'''

access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]
dictionary = {'access': [access_template, 'Введите номер VLAN: '], 'trunk': [trunk_template, 'Введите разрешенные '
                                                                                             'VLANы:']}
int_mode = input("Введите режим работы интерфейса (access/trunk): ")

int_type = input("Введите тип и номер интерфейса: ")
int_vlan = input(dictionary[int_mode][1])

K
print("interface", int_type)
print('\n'.join(dictionary[int_mode][0]).format(int_vlan))
