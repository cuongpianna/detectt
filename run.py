from string import digits
from flask import Flask, render_template, request, jsonify
from googletrans import LANGCODES
from newspaper import Article
from langdetect import detect
import requests
from bs4 import BeautifulSoup
import time
import langid

url = "https://www.vietnamairlines.com/vn/en/home"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
rq = requests.get(url, headers=headers).text
soup = BeautifulSoup(rq, 'html.parser')

tags = ['style', 'script', 'head', 'title', 'meta', 'input', 'iframe', 'img', 'noscript']

for t in tags:
    [s.extract() for s in soup(t)]

results = []


b = ['hello', 'cuong' ,'nguyễn']
for e in  b:
    print(langid.classify(e))