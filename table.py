from requests_api import *
import time

# Частота обращения к api, пока не сформирован результат
t_sleep = 0.3


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
    print(data['nlp'])

    for i in range(len(data['nlp'])):
        temp = get_valid_paragraph(data['phrases'], data['nlp'][i]['sentences'])

        # проверяем валидность абзаца
        if temp['key phrases']:
            temp['paragraph num'] = i + 1
            sent_arr = []

            for j in data['nlp'][i]['sentences']:
                sent = {'text': j['text']}

                dt, ent, kw = [], [], []
                # Заполняем поля datetime и пр. сущности для каждого предложения
                print(j['lemmas'])
                for k in data['nlp'][i]['entities']:
                    print(k)
                    K_temp = k['name'].lower().split()
                    check = True

                    for m in K_temp:
                        if m not in j['lemmas']:
                            check = False

                    if check:
                        if (k['type'] == 'date' or k['type'] == 'time') and k['name'] not in dt:
                            dt.append(k['name'])

                        elif k['name'] not in ent:
                            ent.append(k['name'])

                # Заполняем keywords, которые встретились у конкретного предложения
                for k in data['nlp'][i]['keywords']:
                    for m in k['phrase'].split('|'):
                        if m not in kw and m in j['lemmas']:
                            kw.append(m)

                sent.update({'date/time': dt, 'rest entities': ent, 'keywords': kw})
                sent_arr.append(sent)
                (print('\n\n'))
            temp['sentences'] = sent_arr
            Table.append(temp)

    return {"data": Table}
