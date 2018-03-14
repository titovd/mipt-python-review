import random
import re
import argparse
import json
import os
import sys

# Случайный выбор начального слова или же в случае,
# когда множество слов, следующих за <слово1>, пусто


def generate_start(model):
    tmp_list = list(model.keys())
    return random.choice(tmp_list)


# Генерация следующего за данным словом слова
# Используется проедложенное кумулятивное распределение


def generate_next_word(word_model):
    total = sum(word_model.values())
    random_int = random.randint(0, total - 1)
    index = 0
    list_of_keys = list(word_model.keys())
    for i in range(0, len(word_model.keys())):
        index += word_model[list_of_keys[i]]
        if index >= random_int:
            return list_of_keys[i]


# Генерирование последовательности заданной длины
# для заданного начального слова
# В случае отсутствия заданного начального слова выбираем его случайно


def generate_sentence(length, model, start):
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


# Открытие модели


def open_file(model):
    my_file = open(model, mode='r')
    data = json.load(my_file)
    my_file.close()
    return data


parser = argparse.ArgumentParser(description='Sentence generator')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    metavar='',
                    help='The path to the model')
parser.add_argument('-l',
                    '--length',
                    type=int,
                    metavar='',
                    help='The length of the sentence')
parser.add_argument('-o',
                    '--output',
                    type=str,
                    metavar='',
                    nargs='?',
                    help='The path to the file with the result')
parser.add_argument('-s',
                    '--seed',
                    type=str,
                    metavar='',
                    nargs='?',
                    default='',
                    help='The first word of your sentence')
args = parser.parse_args()


# Открытие созданной модели и генирирование предложения


if __name__ == '__main__':
    data = open_file(args.model)
    if args.output:
        my_file = open(args.output, mode='w', encoding='UTF-8')
        if args.seed:
            sentence = generate_sentence(args.length, data, args.seed) + '\n'
            my_file.write(sentence)
            my_file.close()
        else:
            start = generate_start(data)
            sentence = generate_sentence(args.length, data, start) + '\n'
            my_file.write(sentence)
            my_file.close()
    else:
        if args.seed:
            sentence = generate_sentence(args.length, data, args.seed) + '\n'
            sys.stdout.write(sentence)
        else:
            start = generate_start(data)
            sentence = generate_sentence(args.length, data, args.seed) + '\n'
            sys.stdout.write(sentence)
