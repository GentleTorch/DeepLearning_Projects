# -*- coding: utf-8 -*-

"""
version:    python3.6
author:     ailab
license:    Apache Licence 
contact:    JesusLeaf@163.com
site:       https://github.com/HardWorkingLeaf
software:   PyCharm
file:       spyder.py
time:       2019/8/15 上午8:29

description: 


"""

import os
import re
import urllib
import shutil
import requests
import itertools
import argparse

# ------------------------ URL decoding ------------------------
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# ------------------------ Encoding ------------------------
def decode(web_url):
    for key, value in str_table.items():
        web_url = web_url.replace(key, value)
    return web_url.translate(char_table)


# ------------------------ Page scroll down ------------------------
def build_urls(key_word):
    word = urllib.parse.quote(key_word)
    web_url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={" \
              r"word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60 "
    web_urls = (web_url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return web_urls


re_url = re.compile(r'"objURL":"(.*?)"')


# ------------------------ Get imgURL ------------------------
def resolve_img_url(web_url):
    img_urls = [decode(x) for x in re_url.findall(web_url)]
    return img_urls


# ------------------------ Download imgs ------------------------
def download_images(img_url, dir_path, img_name, save_type='.jpg'):
    filename = os.path.join(dir_path, img_name)
    try:
        res = requests.get(img_url, timeout=15)
        if str(res.status_code)[0] == '4':
            print(str(res.status_code), ":", img_url)
            return False
    except Exception as e:
        print(e)
        return False
    with open(filename + save_type, 'wb') as f:
        f.write(res.content)


# ------------------------ Check save dir ------------------------
def mkdir(save_dir):
    try:
        shutil.rmtree(save_dir)
    except:
        pass
    os.makedirs(save_dir)


def get_pics(save_dir, key_word, max_num):
    print('\n\n', '= = ' * 25, ' Keyword Spider ', ' = =' * 25, '\n\n')

    # mkdir()
    urls = build_urls(key_word)
    idx = 0
    for url in urls:
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolve_img_url(html)
        # Ending if no img
        if len(imgUrls) == 0:
            break
        for web_url in imgUrls:
            download_images(web_url, save_dir, '{:>05d}'.format(idx + 1))
            print('  {:>05d}'.format(idx + 1))
            idx += 1
            if idx >= max_num:
                break
        if idx >= max_num:
            break
    print('\n\n', '= = ' * 25, ' Download ', idx, ' pic ', ' = =' * 25, '\n\n')


# ------------------------ Main ------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download pictures from baidu pics.')
    parser.add_argument('-s', '--save_dir', help='where to save the picture ')
    parser.add_argument('-w', '--key_word', help='what you want to collect pictures')
    parser.add_argument('-n', '--num', help='how many pictures you want to download')

    args = parser.parse_args()
    if args.save_dir is None:
        print('we need variable: save_dir')
        exit(0)
    if args.key_word is None:
        print('we need variable: key_word')
        exit(0)
    if args.num is None:
        print('we need variable: num')
        exit(0)

    get_pics(args.save_dir, args.key_word, int(args.num))
