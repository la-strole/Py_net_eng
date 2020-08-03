import telnetlib
import time
import ipaddress
import re
import math

def telnet_with_router(ip, commands: list, sleep_delay=4):
    """ telnet session with router"""
    print(f'telnet connection to remote server ip = {ip}')
    t = telnetlib.Telnet(str(ip))
    print(f'telnet connection successful\nauthentication..')
    t.read_until(b'Login: ', timeout=5)
    t.write(b'admin\n')
    t.read_until(b'Password: ', timeout=5)
    t.write(b'ithimaniso\n')
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
    print('take networks info')
    header_networks_table = [('SSID name', 'MAC address', 'Channel number', 'Mode', 'Quality'), ]
    # find string like "Dlink77   c0:4a:00:6f:18:06   6    11b/g/n    39"
    networks_list = re.compile(r'(?P<network_name>[\w -]+)\s{2,}'
                               '(?P<mac_address>(?:\w{2}:){5}\w{2})\s{2,}'
                               '(?P<channel_number>\d+)\s{2,}'
                               '(?P<mode>\d{2}\S+)\s{2,}'
                               '(?P<quality>\d+)')
    result = re.findall(networks_list, string)
    return header_networks_table + result


def take_arp_table(string):
    print('take arp table')
    arp_table_pattern = re.compile(r'(?P<ip_address>(?:\d+\.){3}\d+)(?:\s+)'
                                   r'(?P<mac_address>(?:\w{2}:){5}\w{2})')
    arp_table = re.findall(arp_table_pattern, string)
    # reverse key - value to mac address be a key in returned dictionary
    arp_table = [(mac, ip) for ip, mac in arp_table]
    return dict(arp_table)


def ping_remote_hosts(ip_list: list, count_ping_packet=30):
    return_dict = {}
    command = [f'tools ping {ip} count {count_ping_packet}\n' for ip in ip_list]
    print(f'ping remote host')
    output = telnet_with_router(router_ip, command, sleep_delay=20)
    if output:
        result = re.compile(r'(?:.+from (\d+\.\d+\.\d+\.\d+).+time=(\d+\.\d{2}) ms)')
        out = re.findall(result, output)
        for item in out:
            if item[0] not in return_dict.keys():
                return_dict[item[0]] = [item[1]]
            else:
                return_dict[item[0]].append(item[1])
        return return_dict
    else:
        return ValueError


def ping_delay_analyze(results: list):
    # sort list
    sorted_results = sorted([float(x) for x in results])
    count_receive = len(sorted_results)
    # count - global from main - count of ping packets
    packet_loss_percent = count_receive / count
    if packet_loss_percent > 0.3:
        print(f'packet loss = {packet_loss_percent*100} %')
        return -1
    # TODO hard mistakes analyze here (before math exp etc)
    upn = {10: 0.41, 15: 0.34, 20: 0.3, 30: 0.26, 100: 0.2}
    list_round = [abs(item-count_receive) for item in sorted(upn.keys())]
    most_close_upn = upn[sorted(upn.keys())[list_round.index(min(list_round))]]

    criteria1_hard_mistake = sorted_results[1] - sorted_results[0]

    number_of_discret = math.floor(1 + 3.2 * math.log10(count_receive))
    width_number = sorted_results[-1] - sorted_results[0]


if __name__ == '__main__':
    router_ip = ipaddress.ip_address('192.168.1.1')
    mac_addresses = {'yandex_station': 'd4:12:43:0e:67:71',
                     'Nata_notebook': '28:e3:47:cd:6e:0d',
                     'My_notebook': '20:68:9d:46:22:c3'}

    command_list = ['show site-survey WifiMaster0\n',
                    'show associations\n',
                    'show ip arp\n']
    output = (telnet_with_router(router_ip, command_list))
    with open('neighbor_wifi.csv', 'w') as file:
        # print(output)
        neighbor_networks = take_networks_info(output)
        for item in neighbor_networks:
            string = list(item)
            string[0] = string[0].rstrip()
            file.write(','.join(string) + '\n')
    # dictionary keys - mac, values - ip
    arp_table = take_arp_table(output)
    count = 30
    ping_result = ping_remote_hosts([arp_table[mac] for mac in mac_addresses.values()], count)
    print(ping_result)
