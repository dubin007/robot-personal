import os
import re

def move_image(img_path, new_img_path):
    os.rename(img_path, new_img_path)

def check_image(title):
    return title.find('.png') != -1

def check_identify(text):
    return len(re.findall('谣言|辟谣|假消息|假的', text)) > 0
