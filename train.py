import random
import re
import argparse
import json
import os
import sys


def generate_lines(data, lowercase):
    """Генератор для считывания данных"""
    for line in data:
        if lowercase:
            yield line.lower()
        else:
            yield line


def generate_lines_stdin():
    for line in sys.stdin:
        yield line


def generate_tokens(lines):
    """Генератор для слов (только кириллица)"""
    for line in lines:
        for token in re.compile(u'[а-яА-Я]+').findall(line):
            yield token


def generate_grams(tokens):
    """Генератор пар слов <слово1>-<слово2>"""
    word_1 = ''
    for word_2 in tokens:
        yield word_1, word_2
        word_1 = word_2


def generate_model(corpus, model, lowercase):
    """Создание модели"""
    lines = generate_lines(corpus, lowercase)
    tokens = generate_tokens(lines)
    grams = generate_grams(tokens)
    for token_1, token_2 in grams:
        if not token_1 or not token_2:
            continue
        if token_1 in model:
            if token_2 in model[token_1]:
                model[token_1][token_2] += 1
            else:
                model[token_1][token_2] = 1
        else:
            model[token_1] = {token_2: 1}


def save_model(model, path):
    """Сохранение модели в указанную директорию"""
    with open(path, mode='w') as file:
        json.dump(model, file, indent=2, ensure_ascii=False)


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


def main():
    """Создание словаря, считывание данных
        (из файла или же со стандартного потока ввода)
        Обработка входных данных,
        создание и сохранение модели в указанную директорию"""
    model = dict()
    if not args.input_dir:
        print("Введите свой текст здесь\n")
        data = generate_lines_stdin()
        generate_model(data, model, args.lc)
    else:
        for d, dirs, files in os.walk(args.input_dir):
            for file_name in files:
                path = os.path.join(d, file_name)
                with open(path, mode='r', encoding='UTF-8') as file_data:
                    generate_model(file_data, model, args.lc)
    save_model(model, args.model)


if __name__ == '__main__':
    main()
