from string import digits

import requests
from textblob import TextBlob
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate
from langid import classify


def crawl(url):
    """
    Send request and get raw_html from page, support User Agent fake
    :param url:
    :return: raw_html
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    rq = requests.get(url, headers=headers).text
    return rq


def format_html(html):
    """
    Format html, remove digit, special tag, charactor
    :param html:
    :return: Beautiful Soup object
    """
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find('body')
    tags = ['style', 'script', 'head', 'title', 'meta', 'input', 'iframe', 'img', 'noscript']
    for tag in tags:
        [s.extract() for s in soup(tag)]

    return soup


CHARACTOR = ['?', '/', ':', '.', ',', ':', '"', "'", ')', '(', '^', '`', '~', '!', '!', '@', '#', '$', '%', '&', '*',
             '-', '_', '+', '-', '\\', '|', '©']


def hanlde_string(param):
    for c in CHARACTOR:
        param = param.replace(c, '')
    result = param
    return result


def run(url, code):
    """

    :param url:
    :param code:
    :return:
    """
    soup = format_html(crawl(url))
    all_tags = set()
    for tag in soup.find_all():
        all_tags.add(tag)
    results = []
    i = 0
    for tag in all_tags:
        # print(tag.attrs)
        i = i + 1
        if i == 50:
            break
        result_tag = []
        tag_handle = hanlde_string(tag.text)
        remove_digits = str.maketrans('', '', digits)
        tag_handle = tag_handle.translate(remove_digits).strip()
        tag_handle = tag_handle.split(' ')
        for text in tag_handle:
            if len(text) > 2:
                mod = TextBlob(text)
                lang = mod.detect_language()
                if lang != code and text:
                    result_tag.append({
                        'text': text,
                        'lang': lang
                    })

        if result_tag:
            results.append({
                'tag_name': tag.name,
                'tag_class': tag.attrs['class'] if 'class' in tag.attrs else '',
                'errors': result_tag
            })

    return results


results = run('https://www.vietnamairlines.com/vn/vi/home',
              'vi')
for r in results:
    print('------------')
    print('\n')
    print(r)
