from string import digits
from flask import Flask, render_template, request, jsonify
from googletrans import LANGCODES
from newspaper import Article
from langdetect import detect as dtect
from polyglot.detect import Detector
from langid import classify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

CHARACTOR = ['?', '/', ':', '.', ',', ':', '"', "'", ')', '(', '^', '`', '~', '!', '!', '@', '#', '$', '%', '&', '*',
             '-', '_', '+', '-', '\\', '|',]


def hanlde_string(param):
    for c in CHARACTOR:
        param = param.replace(c, '')
    result = param
    return result


@app.route('/')
def index():
    languages = LANGCODES
    return render_template('index.html', languages=languages)


@app.route('/detect', methods=['POST'])
def detect():
    result = []
    if request.method == 'POST':
        url = request.form['url']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        rq = requests.get(url, headers=headers).text

        soup = BeautifulSoup(rq, 'html.parser')

        tags = ['style', 'script', 'head', 'title', 'meta', 'input', 'iframe', 'img', 'noscript']

        for t in tags:
            [s.extract() for s in soup(t)]

        lang = request.form['lang']
        para = soup.html

        i = 0
        for tag in para.find_all():
            i = i + 1
            lst_string = tag.text
            lst_string = hanlde_string(lst_string)
            remove_digits = str.maketrans('', '', digits)
            lst_string = lst_string.translate(remove_digits)
            lst_string = lst_string.split(' ')
            for item in lst_string:
                try:
                    item = item.strip()
                    item = item.strip('\n')
                    item = item.strip('\t')
                    if item == ' ' or not item and not item:
                        continue
                    if type(item) is str:
                        ln = classify(item)
                        if ln[0] != lang:
                            result.append({
                                ln[0]: item
                            })
                except:
                    print(item)

    if result:
        result = combine(result)

        return jsonify({
            'status': 'fail',
            'data': result
        })
    else:
        return jsonify({
            'status': 'success',
            'data': []
        })


@app.route('/crawl', methods=['POST'])
def crawl():
    if request.method == 'POST':
        url = request.form['url']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        rq = requests.get(url, headers=headers).text

        soup = BeautifulSoup(rq, 'html.parser')

        tags = ['style', 'script', 'head', 'title', 'meta', 'input', 'iframe', 'img', 'noscript']

        for t in tags:
            [s.extract() for s in soup(t)]

        content = str(soup.html)
        return jsonify({
            'status': 'success',
            'data': content
        })


def combine(dictionaries):
    combined_dict = {}
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            combined_dict.setdefault(key, []).append(value)
    return combined_dict


if __name__ == '__main__':
    app.run(port=5000, debug=True)
