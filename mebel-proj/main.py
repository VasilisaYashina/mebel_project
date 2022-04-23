from flask import Flask
from flask import render_template
import json
from flask import url_for
from flask import request

app = Flask(__name__)


@app.route('/')
def news():
    with open("package.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('notes.html', news=news_list)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
