from string import digits

import requests
from textblob import TextBlob
from bs4 import BeautifulSoup
from langid import classify
from langdetect import detect


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
             '-', '_', '+', '-', '\\', '|',]


def hanlde_string(param):
    for c in CHARACTOR:
        param = param.replace(c, '')
    result = param
    return result


def run(url, code):
    soup = format_html(crawl(url))
    results = []
    for tag in soup.find_all(recursive=True):
        result_tag = []
        tag_handle = hanlde_string(tag.text)
        remove_digits = str.maketrans('', '', digits)
        tag_handle = tag_handle.translate(remove_digits).strip()
        tag_handle.strip('\n')
        tag_handle.strip('\t')
        text_list = tag_handle.split(' ')
        if text_list:
            for text in text_list:
                print(text)
                print(detect(text))
        #     if len(text) > 1:
        #         lang = detect(text)
        #         if lang != code:
        #             result_tag.append(text)
        #
        # if result_tag:
        #     results.append({
        #         'tag': tag.name,
        #         'text': result_tag
        #     })
        #
        # for r in results:
        #     print(r)

run('https://kenh14.vn/nong-ha-noi-cho-hoc-sinh-mam-non-den-thpt-nghi-tiep-den-8-3-20200226131135824.chn', 'vi')

