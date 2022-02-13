from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from table import *
from create_xlsx import *

app = Flask(__name__)
CORS(app)


@app.route('/nlp/table', methods=['POST'])
def main():
    # Разбиение текста на фразы, на абзацы
    Phrases = request.get_json()["phrases"].split(',')
    Paragraphs = request.get_json()["text"].split("\n\n")

    return create_table(get_data(Phrases, Paragraphs))


@app.route('/nlp/xlsx', methods=['POST'])
def xlsx():
    create_xlsx(main())
    return send_from_directory('tmp', path=os.listdir('tmp/')[-1])


@app.route('/')
def info():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host=os.getenv('HOST'), port=os.getenv("PORT"))
