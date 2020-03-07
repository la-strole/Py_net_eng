# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


def ping_ip_addresses(ip_list):
    """ return tuple - accessable ip address/unaccessable ip address """
    import subprocess
    ret_value = ([], [])
    for ip in ip_list:
        result = subprocess.run(['ping', '-n', '3', ip], stdout=subprocess.PIPE, encoding='866')
        if '100% потерь' in result.stdout:
            ret_value[0].append(ip)
        else:
            ret_value[1].append(ip)
    return ret_value


if __name__ == "__main__":
    from task_12_2 import convert_ranges_to_ip_list
    ip_set = ['127.0.0.1', '172.0.0.1-5']
    print(ping_ip_addresses(convert_ranges_to_ip_list(ip_set)))