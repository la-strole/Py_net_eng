#! /usr/bin/python3
import subprocess
import ipaddress
import time


def ping_alice(alice_ip, router_ip, packet_count, max_wifi_delay, max_internet_delay, loss_persent,
               trust_internet_address='google.com'):
    """ alice_ip - yandex_station ip, ping router and alice return csv values"""
    current_time = time.strftime("%D, %H:%M:%S", time.localtime())
    result_ping_router = subprocess.run(['ping', f'{router_ip}', '-c', f'{packet_count}'], stdout=subprocess.PIPE,
                                        encoding='utf-8')
    if result_ping_router.returncode == 0:
        result_ping_internet = subprocess.run(['ping', f'{trust_internet_address}', '-c', f'{packet_count}'],
                                              stdout=subprocess.PIPE, encoding='utf-8')
        if result_ping_internet.returncode == 0:
            line_ping = result_ping_internet.stdout.split()
            internet_packet_loss = line_ping[-10]
            internet_delay = str(line_ping[-2])
            try:
                int(internet_packet_loss[:-1])
                float(internet_delay.split('/')[1])
            except ValueError:
                ret_string = f'internet_value_error, {current_time}, {internet_packet_loss[:-1]}\n'
                return ret_string
            if int(internet_packet_loss[:-1]) > loss_persent:
                ret_string = f'high_internet_loss, {current_time}, {internet_packet_loss}\n'
                return ret_string
            elif float(internet_delay.split('/')[1]) > max_internet_delay:
                ret_string = f'high_internet_delay, {current_time}, {internet_delay}\n'
                return ret_string
            else:
                result_ping_alice = subprocess.run(['ping', f'{alice_ip}', '-c', f'{packet_count}'],
                                                   stdout=subprocess.PIPE, encoding='utf-8')
                if result_ping_alice.returncode == 0:
                    line_ping = result_ping_alice.stdout.split()
                    alice_packet_loss = line_ping[-10]
                    alice_delay = str(line_ping[-2])
                    try:
                        int(alice_packet_loss[:-1])
                        float(alice_delay.split('/')[1])
                    except ValueError:
                        ret_string = f'alice_value_error, {current_time}, {alice_packet_loss[:-1]}\n'
                        return ret_string
                    if int(alice_packet_loss[:-1]) > loss_persent:
                        ret_string = f'high_alice_loss, {current_time}, {alice_packet_loss}\n'
                        return ret_string
                    elif float(alice_delay.split('/')[1]) > max_wifi_delay:
                        ret_string = f'high_alice_delay, {current_time}, {alice_delay}\n'
                        return ret_string
                    else:
                        ret_string = f'alice_OK, {current_time}, alice_OK\n'
                        return ret_string
                else:
                    ret_string = f'alice_death, {current_time}, {result_ping_alice.returncode}\n'
                    return ret_string
        else:
            ret_string = f'internet_death, {current_time}, {result_ping_internet.returncode}\n'
            return ret_string
    else:
        ret_string = f'notebook_death, {current_time}, {result_ping_router.returncode}\n'
        return ret_string


def main():
    alice_ip = ipaddress.ip_address('192.168.1.33')
    router_ip = ipaddress.ip_address('192.168.1.1')
    packet_count = 3
    trust_internet_address = 'google.com'
    normal_delay_wifi = 100
    normal_delay_internet = 150
    max_persent_loss = 10
    time_period_sec = 60*60*5
    start = time.time()
    while True:
        with open('/home/zzz/Downloads/alice_ping.csv', 'a') as file:
            file.write(ping_alice(alice_ip, router_ip, packet_count, normal_delay_wifi, normal_delay_internet,
                                  max_persent_loss, trust_internet_address))
        time.sleep(120)
        if time.time() > start + time_period_sec:
            break


if __name__ == "__main__":
    main()
