def find_list_of_better_channel_numbers(current_channel, neighbor_networks:dict):
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
    print(sort_best_channels)

current_channel = '10'
neighbor_networks = {'9': ['60'], '6': ['51', '0'], '1': ['39', '15', '5', '0'], '11': ['24', '24', '10', '10'],
                     '4': ['10'], '7': ['0']}

find_list_of_better_channel_numbers(current_channel, neighbor_networks)