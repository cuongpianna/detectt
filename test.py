from flask import Flask, render_template, request, jsonify
from googletrans import Translator, LANGCODES
from newspaper import Article

app = Flask(__name__)


@app.route('/')
def index():
    languages = LANGCODES
    return render_template('index.html', languages=languages)


@app.route('/detect', methods=['POST'])
def detect():
    result = []
    if request.method == 'POST':
        lang = request.form['lang']
        para = request.form['para']
        if not para:
            return jsonify({
                'status': 'success',
                'data': []
            })
        lst_string = para.split(' ')
        for item in lst_string:
            print(item)
            tran = Translator()
            ln = tran.detect(item)
            if ln.lang != lang:
                result.append({
                    ln.lang: item
                })


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
        article = Article(url)
        article.download()
        article.parse()
        content = article.text

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
    app.run(port=7000 ,debug=True)
