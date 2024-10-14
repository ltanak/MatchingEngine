from flask import Flask, redirect, url_for, request, render_template, make_response
import random
import json
from time import time
from random import random

app = Flask(__name__)

# @app.route('/success/<name>')
# def success(name):
#     return 'welcome %s' % name


# @app.route('/', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name=user))
    
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True)