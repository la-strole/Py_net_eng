import telnetlib
import time
import ipaddress
import re


def telnet_with_router(ip, commands: list, sleep_delay=4):
    """ telnet session with router"""
    t = telnetlib.Telnet(str(ip))
    t.read_until(b'Login: ', timeout=5)
    t.write(b'admin\n')
    t.read_until(b'Password: ', timeout=5)
    t.write(b'ithimaniso\n')
    t.read_until(b'(config)>')
    for command in commands:
        t.write(command.encode('utf-8'))
        time.sleep(sleep_delay)
    t.write(b'exit\n')
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


def ping_remote_hosts(ip_list: list):
    return_dict = {}
    for ip in ip_list:
        command = f'tools ping {ip} count 10\n'
        print(f'ping remote host, ip ={ip}')
        output = telnet_with_router(router_ip, [command], sleep_delay=20)
        pattern = re.compile(r'(?P<percent_loss>\d+)(?:%.+\n.+\n.+max = )'
                             r'(?P<delay>\d+.+\d+)')
        result = re.findall(pattern, output)
        if result:
            result[1] = result[1].split('/')
            return_dict[ip] = result
        else:
            return_dict[ip] = 'None'
    return return_dict
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
    print(ping_remote_hosts([arp_table[mac] for mac in mac_addresses.values()]))