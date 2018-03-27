import random
import re
import argparse
import json
import os
import sys


def generate_start(model):
    """Случайный выбор начального слова или же в случае,
    когда множество слов, следующих за <слово1>, пусто"""
    tmp_list = list(model.keys())
    return random.choice(tmp_list)


def generate_next_word(word_model):
    """Генерация следующего за данным словом слова
    Используется проедложенное кумулятивное распределение"""
    total = sum(word_model.values())
    random_int = random.randint(0, total - 1)
    index = 0
    list_of_keys = list(word_model.keys())
    for i in range(0, len(word_model.keys())):
        index += word_model[list_of_keys[i]]
        if index >= random_int:
            return list_of_keys[i]


def generate_sentence(length, model, start):
    """Генерирование последовательности заданной длины
    для заданного начального слова
    В случае отсутствия заданного начального слова выбираем его случайно"""
    if start:
        current_word = start
    else:
        current_word = generate_start(model)
    sentence = str(current_word).capitalize()
    for i in range(0, length):
        if not model.get(current_word):
            new_word = generate_start(model)
        else:
            new_word = generate_next_word(model[current_word])
        current_word = new_word
        sentence += ' ' + current_word
    return sentence + '.'


def open_file(model):
    """Открытие модели"""
    with open(model, mode='r') as file:
        data = json.load(file)
    return data


parser = argparse.ArgumentParser(description='Генератор предложений')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    metavar='',
                    required=True,
                    help='Путь к сохраненной модели')
parser.add_argument('-l',
                    '--length',
                    type=int,
                    metavar='',
                    required=True,
                    help='Длина генерируемой последовательности')
parser.add_argument('-o',
                    '--output',
                    type=str,
                    metavar='',
                    nargs='?',
                    help='Путь к файлу, в который будет записан результат')
parser.add_argument('-s',
                    '--seed',
                    type=str,
                    metavar='',
                    nargs='?',
                    default='',
                    help='Начальное слово последовательности')
args = parser.parse_args()


if __name__ == '__main__':
    """Открытие созданной модели и генирирование предложения"""
    data = open_file(args.model)
    if args.output:
        with open(args.output, mode='w', encoding='UTF-8') as file:
            if args.seed:
                sentence = generate_sentence(args.length, data, args.seed) + '\n'
                file.write(sentence)
            else:
                start = generate_start(data)
                sentence = generate_sentence(args.length, data, start) + '\n'
                file.write(sentence)
    else:
        if args.seed:
            sentence = generate_sentence(args.length, data, args.seed) + '\n'
            sys.stdout.write(sentence)
        else:
            start = generate_start(data)
            sentence = generate_sentence(args.length, data, args.seed) + '\n'
            sys.stdout.write(sentence)
