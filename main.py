from flask import Flask, request
from flask_cors import CORS
import requests
import time

URL = "http://newnlp.cogsys.company/api/v1/"
app = Flask(__name__)
CORS(app)
t_sleep = 0.3  # Частота обращения к api, пока не сформирован результат


################################################### Запросы к api ######################################################

def get_status(task_id):
    return requests.get(f"{URL}nlp/{task_id}/status").json()['status']


def get_result(task_id):
    return requests.get(f"{URL}nlp/{task_id}/result").json()['result']


def post_lemmas(text):
    return requests.post(f"{URL}nlp/lemmas", json={"text": text}).json()


def post_nlp(text):
    return requests.post(f"{URL}nlp", json={"text": text}).json()


########################################################################################################################

def get_data(phrases, paragraphs):
    # Нахождение лемм для ключевых фраз
    Lemmas_phrases = []
    for el in phrases:
        req = post_lemmas(el)
        task_id = req['result']

        while get_status(task_id) == 'PENDING':
            time.sleep(t_sleep)

        if get_status(task_id) == 'SUCCESS':
            Lemmas_phrases.append({'text': el, 'lemmas': get_result(task_id)['lemmas']})

    # Прогоняем абзацы через апишку и находим леммы для каждого предложения
    Nlp_paragraphs = []
    for el in paragraphs:
        req = post_nlp(el)
        task_id = req['result']

        while get_status(task_id) == 'PENDING':
            time.sleep(t_sleep)

        if get_status(task_id) == 'SUCCESS':
            res = get_result(task_id)
            Nlp_paragraphs.append(res)

            for sen in res['sentences']:
                req = post_lemmas(sen['text'])
                task_id = req['result']

                while get_status(task_id) == 'PENDING':
                    time.sleep(t_sleep)

                if get_status(task_id) == 'SUCCESS':
                    sen['lemmas'] = get_result(task_id)['lemmas']

    return {"phrases": Lemmas_phrases, "nlp": Nlp_paragraphs}


def get_valid_paragraph(phrases, keywords):
    result, all_kw = [], []

    for i in keywords:
        all_kw.extend(i['lemmas'])

    for el in phrases:
        check = True

        for lem in el['lemmas']:
            if lem not in all_kw:
                check = False

        if check:
            result.append(el['text'])

    return {"key phrases": result}


def create_table(data):
    Table = []
    # print(data['nlp'])

    for i in range(len(data['nlp'])):
        temp = get_valid_paragraph(data['phrases'], data['nlp'][i]['sentences'])

        if temp['key phrases']:                                                         # проверяем валидность абзаца
            temp['paragraph num'] = i + 1
            sent_arr = []

            for j in data['nlp'][i]['sentences']:
                sent = {'text': j['text']}

                dt, ent, kw = [], [], []
                for k in data['nlp'][i]['entities']:  # Заполняем поля datetime и пр. сущности для каждого предложения

                    if k['name'].lower() in j['lemmas']:
                        if (k['type'] == 'date' or k['type'] == 'time') and k['name'] not in dt:
                            dt.append(k['name'])

                        elif k['type'] not in ent:
                            ent.append(k['type'])

                for k in data['nlp'][i]['keywords']:  # Заполняем keywords, которые встретились у конкретного предложения
                    for m in k['phrase'].split('|'):
                        if m not in kw and m in j['lemmas']:
                            kw.append(m)

                sent.update({'date/time': dt, 'rest entities': ent, 'keywords': kw})
                sent_arr.append(sent)

            temp['sentences'] = sent_arr
            Table.append(temp)

    return {"data": Table}


@app.route('/nlp/table', methods=['POST'])
def main():
    Phrases = request.get_json()["phrases"].split(',')          # Разбиение текста на фразы
    Paragraphs = request.get_json()["text"].split("\n\n")       # Разбиение текста на абзацы
    Data = get_data(Phrases, Paragraphs)                        # Прогоняем данные через api
    Table = create_table(Data)                                  # Создаём таблицу с результатом

    return Table


@app.route('/')
def info():
    return "You can do only post request ../nlp/table with 2 parameters(phrases, text)"


if __name__ == "__main__":
    app.run()