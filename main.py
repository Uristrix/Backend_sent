from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from table import *
from create_xlsx import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/nlp/table', methods=['POST'])
def table():
    # Разбиение текста на фразы, на абзацы
    Req = request.get_json()
    Phrases = Req["phrases"].split(',')
    Paragraphs = Req["text"].split("\n\n")

    # Выделение дополнительных фраз
    Req.pop('text')
    Req.pop('phrases')
    other_phrases = {}
    for el in Req:
        other_phrases[el] = Req[el].split(',')
    Table = create_table(get_data(Phrases, Paragraphs, other_phrases))

    return Table


@app.route('/nlp/xlsx', methods=['POST'])
def xlsx():
    create_xlsx(table())
    dirr = os.listdir('tmp/')
    num = max([int(el[4:-5]) for el in dirr])
    return send_from_directory('tmp', path=f'file{num}.xlsx')


if __name__ == "__main__":
    app.run(host=os.getenv('HOST'), port=os.getenv("PORT"))
