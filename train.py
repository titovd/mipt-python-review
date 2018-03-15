import random
import re
import argparse
import json
import os
import sys

# Рассматриваем только символы алфавита русского языка
# Прописные и строчные буквы


r_alphabet = re.compile(u'[а-яА-Я]+')

parser = argparse.ArgumentParser(description='Создание и сохранение модели')
parser.add_argument('-in',
                    '--input-dir',
                    type=str,
                    metavar='',
                    nargs='?',
                    help='Путь к директории с текстами(.txt)')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    metavar='',
                    required=True,
                    help='Путь к файлу, в который сохраняется модель')
parser.add_argument('--lc',
                    action='store_true',
                    help='Приводить ли тексты к lowercase')
args = parser.parse_args()

is_lowercase = args.lc


# Генераторы для считывания данных


def generate_lines(data):
    for line in data:
        yield line


def generate_lower_lines(data):
    for line in data:
        yield line.lower()


def generate_lines_stdin():
    for line in sys.stdin.readlines():
        yield line


# Генератор для слов (только кириллица)


def generate_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


# Генератор пар слов <слово1>-<слово2>


def generate_grams(tokens):
    word_1, word_2 = '#', '#'
    for word_2 in tokens:
        yield word_1, word_2
        word_1 = word_2


# Создание модели


def generate_model(corpus, my_model, lowercase):
    if is_lowercase:
        lines = generate_lower_lines(corpus)
    else:
        lines = generate_lines(corpus)
    tokens = generate_tokens(lines)
    grams = generate_grams(tokens)
    for t1, t2 in grams:
        if t1 == '#' or t2 == '#':
            continue
        if t1 in my_model:
            if t2 in my_model[t1]:
                my_model[t1][t2] += 1
            else:
                my_model[t1][t2] = 1
        else:
            my_model[t1] = {t2: 1}


# Сохранение модели в указанную директорию


def save_model(model, path):
    model_dir = path
    my_file = open(model_dir, mode='w')
    json.dump(model, my_file, indent=2, ensure_ascii=False)
    my_file.close()


# Создание словаря, считывание данных
# (из файла или же и стандартного потока ввода)
# Обработка входных данных, создание и сохранение модели в указанную директорию


if __name__ == '__main__':
    model = dict()
    if not args.input_dir:
        print("Enter your text here\n")
        data = generate_lines_stdin()
        generate_model(data, model, args.lc)
    else:
        for d, dirs, files in os.walk(args.input_dir):
            for file_data in files:
                path = os.path.join(d, file_data)
                file_data = open(path, mode='r', encoding='UTF-8')
                generate_model(file_data, model, args.lc)
                file_data.close()
    save_model(model, args.model)
