import random
import re
import argparse
import json
import os
import sys


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
        current_word = random.choice(list(model.keys()))
    sentence = str(current_word).capitalize()
    for i in range(length):
        if not model.get(current_word):
            new_word = random.choice(list(model.keys()))
        else:
            new_word = generate_next_word(model[current_word])
        current_word = new_word
        sentence += ' ' + current_word
    return sentence + '.'


def load_model(model_path):
    """Открытие модели"""
    with open(model_path, mode='r') as file:
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


def main():
    """Открытие созданной модели и генирирование предложения"""
    data = load_model(args.model)
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
            sentence = generate_sentence(args.length, data, args.seed) + '\n'
            sys.stdout.write(sentence)


if __name__ == '__main__':
    main()
