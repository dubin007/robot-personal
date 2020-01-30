import os
import random
import re

from src.util.constant import INFO_TAILS


def move_image(img_path, new_img_path):
    os.rename(img_path, new_img_path)

def remove_image(image_path):
    os.remove(image_path)

def check_image(title):
    return title.find('.png') != -1

def check_identify(text):
    return len(re.findall('谣言|辟谣|假消息|假的|防控|卫健委|卫生部|指挥部', text)) > 0

def get_random_tail():
    return INFO_TAILS[random.randint(0, 10)]

def get_random_split():
    return random.random() * 6

def get_random_split_short():
    return random.random() * 3

def get_random_long_time():
    return random.random() * 60 * 60
