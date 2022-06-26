# csv_readedr.py

import csv


def csv_reader(filepath):
    with open(filepath, encoding="utf-8") as r_file:
        # Создаем объект DictReader, указываем символ-разделитель ","
        fieldnames = ["Наименование", "Дата", "Цена_1", "Цена_2", "Цена_3", "Цена_4"]
        file_reader = csv.DictReader(r_file, delimiter=",", fieldnames=fieldnames)
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        return list(file_reader)
