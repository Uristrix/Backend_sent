from requests_api import *
import time

# Частота обращения к api, пока не сформирован результат
t_sleep = 0.3


def lemmas(phrases):
    # Нахождение лемм для ключевых фраз
    Lemmas_phrases = []
    for el in phrases:
        req = post_lemmas(el)
        task_id = req['result']

        while get_status(task_id) == 'PENDING':
            time.sleep(t_sleep)

        if get_status(task_id) == 'SUCCESS':
            Lemmas_phrases.append({'text': el, 'lemmas': get_result(task_id)['lemmas']})

    return Lemmas_phrases


def nlp(paragraphs):
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

    return Nlp_paragraphs


def get_data(phrases, paragraphs, other_phrases):
    for el in other_phrases:
        other_phrases[el] = lemmas(other_phrases[el])

    return {"phrases": lemmas(phrases), "nlp": nlp(paragraphs), 'other_phrases': other_phrases}


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
    # for i in range(len(data['nlp'])):
    #     print(data['nlp'][i]['sentences'])

    for i in range(len(data['nlp'])):
        temp = get_valid_paragraph(data['phrases'], data['nlp'][i]['sentences'])
        # проверяем валидность абзаца
        if temp['key phrases']:
            

            temp['paragraph num'] = [str(i + 1)]

            # заполняем предложения
            sent_arr = []
            for j in data['nlp'][i]['sentences']:
                sent = {'text': [j['text']]}

                # проходим по валидным  и ищем в них дополнительные фразы
                for el in data['other_phrases']:
                    temp2 = get_valid_paragraph(data['other_phrases'][el],[j])
                    if temp2:                    
                        sent.update({el : temp2['key phrases']})
                    else:
                        sent.update({el : []})

                dt, ent, kw = [], [], []
                # Заполняем поля datetime и пр. сущности для каждого предложения
                for k in data['nlp'][i]['entities']:
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

                sent.update({'date/time': dt, 'keywords': kw, 'rest entities': ent})
                sent_arr.append(sent)

            temp['sentences'] = sent_arr
            Table.append(temp)

    return {"data": Table}
