import telnetlib
import time
import ipaddress
import re
import math


def telnet_with_router(ip, commands: list, sleep_delay=4):

    """ 
    telnet session with router (OPEN WRT OS). 
    commands - list of string, 
    output - string
    """
    
    print(f'telnet connection to remote server ip = {ip}')
    t = telnetlib.Telnet(str(ip))
    print(f'telnet connection successful\nauthentication..')
    t.read_until(b'Login: ', timeout=5)
    t.write(b'admin\n')
    t.read_until(b'Password: ', timeout=5)
    
    # Change PASSWORD to your router password
    t.write(b'PASSWORD\n')
    
    t.read_until(b'(config)>')
    print('authentication successful')
    for command in commands:
        t.write(command.encode('utf-8'))
        time.sleep(sleep_delay)
    t.write(b'exit\n')
    print(f'close telnet connection to server ip = {ip}')
    out = t.read_very_eager()
    return out.decode('utf-8')


def take_networks_info(string):
    """
    Parse output of telnet command show site-survey WifiMaster0 for neighbor wifi
    """
    
    print('take networks info')
    header_networks_table = [('SSID name', 'MAC address', 'Channel number', 'Mode', 'Quality'), ]
    
    # find string like "Dlink77   c0:4a:00:6f:18:06   6    11b/g/n    39"
    networks_list = re.compile(r'(?P<network_name>[\w -]+)\s{2,}'
                               '(?P<mac_address>(?:\w{2}:){5}\w{2})\s{2,}'
                               '(?P<channel_number>\d+)\s{2,}'
                               '(?P<mode>\d{2}\S+)\s{2,}'
                               '(?P<quality>\d+)')
                               
    result = re.findall(networks_list, string)
    
    if result:
        return header_networks_table + result
    else:
        return -1


def take_arp_table(string):
    """
    Parse output show ip arp, return [(mac, ip)]
    """
    
    print('take arp table')
    arp_table_pattern = re.compile(r'(?P<ip_address>(?:\d+\.){3}\d+)(?:\s+)'
                                   r'(?P<mac_address>(?:\w{2}:){5}\w{2})')
                                   
    arp_table = re.findall(arp_table_pattern, string)
    # reverse key - value to mac address be a key in returned dictionary
    if arp_table:
        arp_table = [(mac, ip) for ip, mac in arp_table]
        return dict(arp_table)
    else:
        return -1


def ping_remote_hosts(ip_list: set, router_ip, count_ping_packet=30):
    """
    Return dictionary {ip_address: [delay_times]}. If host is unreachable - it's ip address in dictionary with
    string host unreachable
    """
    
    return_dict = {}
    command = [f'tools ping {ip} count {count_ping_packet}\n' for ip in ip_list]
    print(f'ping remote host')
    # delay = 40 because of long time ping (approximately 30 sec for 30 icmp packets)
    output = telnet_with_router(router_ip, command, sleep_delay=40)
    if output:
        # if ping ok and host is reachable
        result = re.compile(r'(?:.+from (\d+\.\d+\.\d+\.\d+).+time=(\d+\.\d{2}) ms)')
        out = re.findall(result, output)
        if out:
            for item in out:
                try:
                    if item[0] not in return_dict.keys():
                        return_dict[item[0]] = [item[1]]
                    else:
                        return_dict[item[0]].append(item[1])
                except IndexError:
                    print(f'error in ping remote host function, out = {out}, look at out[0],out[1]')
                    return -1
            for item in ip_list:
                if item not in return_dict.keys():
                    return_dict[item] = ['host unreachable']
            return return_dict
        else:
            print(f'error in ping remote host function, out is empty, mb all remote hosts are unreachable')
            return -1
    else:
        return -1


def ping_delay_analyze(results: list, count):
    """
    Take list of ping delays (mb string), count - number of sent icmp packets,
    then calculate lost percent, then delete mistakes, then calculate expected value
    return -1 if error, 0 if great packet loss, expected value if that's OK
    """
    
    if type(results) == list and len(results) > 1:
        # sort list
        try:
            sorted_results = sorted([float(x) for x in results])
        except ValueError:
            print(f'error in ping_delay_analize function. Can not make float from result list = {results}')
            return -1
        count_receive = len(sorted_results)
        packet_loss_percent = 1 - (count_receive / count)
        if packet_loss_percent > 0.3:
            print(f'packet loss = {packet_loss_percent * 100} %')
            return 0
        # upn - values for different counts to delete hard mistakes
        upn = {10: 0.41, 15: 0.34, 20: 0.3, 30: 0.26, 100: 0.2}
        # looking for the closed value from upn.keys() to count number
        list_round = [abs(item - count_receive) for item in sorted(upn.keys())]
        most_close_upn = upn[sorted(upn.keys())[list_round.index(min(list_round))]]
        # delete hard mistakes
        try:
            while True:
                criteria1_hard_mistake_min = (sorted_results[1] - sorted_results[0]) / (
                        sorted_results[-1] - sorted_results[0])
                if criteria1_hard_mistake_min > most_close_upn:
                    sorted_results.pop(0)
                else:
                    break
            while True:
                criteria1_hard_mistake_max = (sorted_results[-1] - sorted_results[-2]) / (
                        sorted_results[-1] - sorted_results[0])
                if criteria1_hard_mistake_max > most_close_upn:
                    sorted_results.pop(-1)
                else:
                    break
        except IndexError:
            print(f'error in ping_delay_analyze function, then try to delete hard mistakes. Look at Index error.'
                  f'list of results = {sorted_results}')
            return -1
        # calculate expected value
        number_of_discrete = math.floor(1 + 3.2 * math.log10(len(sorted_results)))
        try:
            width_number = sorted_results[-1] - sorted_results[0]
            value_range = [sorted_results[0] + sorted_results[0] * (width_number / number_of_discrete) * (item + 1)
                           for item in range(number_of_discrete)]
        except IndexError:
            print(f'error in ping_delay_analyze function, then try to calculate width_number or value range '
                  f'(in expected value calculating). Look at Index error. list of results = {sorted_results}')
            return -1
        res_range = [[] for item in range(number_of_discrete)]
        # spread values across ranges
        i = 0
        for item in sorted_results:
            while True:
                if item <= value_range[i]:
                    res_range[i].append(item)
                    break
                else:
                    i += 1
        # probability of falling within the ranges
        list_of_probability = list(map(lambda x: len(x) / len(sorted_results), res_range))
        # arithmetic mean over ranges
        avg_list = []
        for item in res_range:
            if len(item) != 0:
                avg_list.append(sum(item) / len(item))
            else:
                avg_list.append(0)
        expected_value = sum([x * y for x, y in zip(avg_list, list_of_probability)])
        return expected_value
    else:
        return -1


def key_from_value(dictionary: dict, value):
    """
    Return key from dictionary's value
    """
    
    if value in dictionary.values():
        output = [k for k, v in dictionary.items() if v == value]
        return output
    else:
        print(f'value not in dictionary {dictionary} values')
        return -1


def define_rssi_for_hosts(output):
    """
    Parse output for rssi. return dictionary [mac] = rssi
    """
    
    rssi_dict = re.findall(r'mac: ((?:\w{2}:){5}\w{2}).+?rssi: -(\d+)', output, re.DOTALL)
    if rssi_dict:
        try:
            return dict(rssi_dict)
        except TypeError:
            print(f'error in define_rssi_for_host function with dict({rssi_dict})')
            return -1
    else:
        return -1


def find_list_of_better_channel_numbers(current_channel, neighbor_networks:dict, current_rssi, current_ping_result:dict,
                                        mac_address_table, router_ip):
    preferred_channels = {}
    for item in range(1, 14):
        item = str(item)
        if item in neighbor_networks.keys():
            summary_neighbor_quality = sum([int(x) for x in neighbor_networks[item]])
        else:
            summary_neighbor_quality = 0
        preferred_channels[item] = summary_neighbor_quality
    best_channel = sorted(['1', '6', '11'], key=lambda x: preferred_channels[x])
    sort_best_channels = []
    for item in best_channel:
        if 50 > preferred_channels[item] and item != current_channel:
            sort_best_channels = [item]
            break
        else:
            del preferred_channels[item]
    else:
        del preferred_channels[str(current_channel)]
        sort_best_channels = sorted(preferred_channels.keys(), key=lambda x: preferred_channels[x])
    # to define new rssi and expected value
    # TODO write change channel number here
    command_to_router = ['show associations\n']
    output = telnet_with_router(router_ip, command_to_router, sleep_delay=3)

    new_rssi = define_rssi_for_hosts(output)
    new_ping_result = ping_remote_hosts(set(current_ping_result.keys()), router_ip, count_ping_packet=5)
    # TODO change ping result funcion to return expected value
    for ip in new_ping_result.keys():
        print(f'expected value {mac_addresses[key_from_value(arp_table, ip)[0]]} = '
              f'{round(ping_delay_analyze(ping_result[ip], count), 2)}')


    # TODO write here list of better channel numbers and try to change channel number -if rssi or ping dalay would be
    # worse - restore old configuration


if __name__ == '__main__':

    router_ip = ipaddress.ip_address('192.168.1.1')
    
    mac_addresses = {'d4:12:43:0e:67:71': 'yandex_station',
                     '28:e3:47:cd:6e:0d': 'Nata_notebook',
                     '20:68:9d:46:22:c3': 'My_notebook',
                     '38:a4:ed:64:74:b5': 'Nata_smartphone'}

    command_list = ['show site-survey WifiMaster0\n',
                    'show associations\n',
                    'show ip arp\n',
                    'show interface\n']

    output = (telnet_with_router(router_ip, command_list))
    
    # define rssi for each host in arp table
    rssi = define_rssi_for_hosts(output)
    if rssi == -1:
        print('error with define rssi')
    else:
        for key in rssi.keys():
            print(f'{mac_addresses[key]} = {rssi[key]} rssi')
    neighbor_networks = take_networks_info(output)
    
    # define dictionary with neighbor networks - d[channel_number] = ['n','n'...], n - quality of signal
    if neighbor_networks != -1:
        neighbor_network_dict = {}
        for item in neighbor_networks[1:]:
            if item[2] not in neighbor_network_dict.keys():
                neighbor_network_dict[item[2]] = [item[4]]
            else:
                neighbor_network_dict[item[2]].append(item[4])
        print(neighbor_network_dict)
    else:
        print(f'error im main section with neighbor_networks. output = {output}')
        
    # dictionary keys - mac, values - ip
    arp_table = take_arp_table(output)
    
    # define current channel number
    pattern_channel = re.compile(r'channel: (\d+)')
    current_channel = re.findall(pattern_channel, output)[0]
    print(f'current channel number = {current_channel}')
    
    # define number of icmp packets to ping remote hosts
    count = 30
    ping_result = ping_remote_hosts(set([arp_table[mac] for mac in mac_addresses.keys() if mac in arp_table.keys()]),
                                    router_ip, count)
                                    
    # TODO current ping result should be a list - not print function
    for ip in ping_result.keys():
        print(f'expected value {mac_addresses[key_from_value(arp_table, ip)[0]]} = '
              f'{round(ping_delay_analyze(ping_result[ip], count), 2)}')
              
    # if yandex station and my notebook rssi >70 and expected value > 100 ms -> time to try another channel number
    # TODO write here code for this condition
    find_list_of_better_channel_numbers(current_channel, neighbor_network_dict, rssi, ping_result, arp_table, router_ip)
