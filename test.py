from flask import Flask, render_template, request, jsonify
from googletrans import LANGCODES
from func import run

app = Flask(__name__)


@app.route('/')
def index():
    languages = LANGCODES
    return render_template('index.html', languages=languages)


@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            results = run(url, 'vi')
            return render_template('result.html', results=results)
    else:
        return "1"


def combine(dictionaries):
    combined_dict = {}
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            combined_dict.setdefault(key, []).append(value)
    return combined_dict


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
