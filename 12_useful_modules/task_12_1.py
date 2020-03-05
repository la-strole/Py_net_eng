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


def ping_ip_addresses(ip_list: list):
    """ return tuple of success and unsuccess ping of addresses from address list"""
    import ipaddress
    import subprocess
    ret_tuple = ([], [])
    for ip in ip_list:
        try:
            ipaddress.ip_address(ip)
            result = subprocess.run(['ping', '-c', '2', ip], stdout=subprocess.PIPE, encoding='utf8')
            if '100% packet loss' in result.stdout:
                ret_tuple[1].append(ip)
            else:
                ret_tuple[0].append(ip)
        except ValueError:
            print(f"error with value {ip}. It seems to be not an ip address")
            return -1
    return ret_tuple


if __name__ == "__main__":
    ip_addresses = ['127.0.0.1', '1.1.1.1', '8.8.8.8', '1.2.3.4', '172.0.0.1']
    print(ping_ip_addresses(ip_addresses))
