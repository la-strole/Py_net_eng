# -*- coding: utf-8 -*-
"""
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого
вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения
(их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml (должен быть создан в предыдущем задании 17.2a).
На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
import yaml
from draw_network_graph import draw_topology


def transform_topology(file_name: str):
    with open(file_name) as f:
        structure = yaml.safe_load(f)
    main_list = {}
    for first in structure.items():
        for second in first[1].items():
            letter = [(key, second[1][key]) for key in second[1].keys()]
            main_list.update({(first[0], second[0]): letter[0]})
    keys = list(main_list.keys())
    for item in keys:
        if item in main_list.values():
            del main_list[item]
    print(main_list)
    return main_list


if __name__ == '__main__':
    name = 'new.yaml'
    draw_topology(transform_topology(name))
