# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция check_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''


def convert_ranges_to_ip_list(ip_list: list):
    """" take list of ip addresses or single ip address like an argument - return list of ip addresses or -1"""
    import ipaddress
    return_list = []
    for ip in ip_list:
        try:
            ip_first = ipaddress.ip_address(ip)
            return_list.append(str(ip_first))
        except ValueError:
            line = ip.split('-')
            try:
                ip_first = ipaddress.ip_address(line[0])
                try:
                    ip_last = ipaddress.ip_address(line[1])
                    item = ip_first
                    while item != ip_last + 1:
                        return_list.append(str(item))
                        item += 1
                except ValueError:
                    try:
                        number = int(line[1])
                        for item in range(number):
                            return_list.append(str(ip_first + item))
                    except ValueError:
                        print(f"something wrong with {line}")
                        return -1
            except ValueError:
                print(f"something wrong with address {line}")
                return -1
    return return_list


if __name__ == "__main__":
    ip_list_input = ['8.8.4.4', '1.1.1.1-7', '172.21.41.128-172.21.41.132']
    print(convert_ranges_to_ip_list(ip_list_input))
