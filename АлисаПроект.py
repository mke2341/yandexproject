# импортируем библиотеки
from flask import Flask, request
import logging
import json

q = 1

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info('Response: %r', request.json)
    return json.dumps(response)

def dnatransk(a):
    seq = ''
    for i in a:
        if i == 'a' or i == 'а':
            seq += 'u'
        elif i == 't' or i == 'т':
            seq += 'a'
        elif i == 'c' or i == 'с':
            seq += 'g'
        elif i == 'g' or i == 'г':
            seq += 'c'
        else:
            seq = 'Напишите нормальную последовательность'
            break
    return seq

def rnarevtransk(a):
    seq = ''
    for i in a:
        if i == 'a':
            seq += 't'
        elif i == 'u':
            seq += 'a'
        elif i == 'c':
            seq += 'g'
        elif i == 'g':
            seq += 'c'
        else:
            seq = 'Напишите нормальную последовательность'
            break
    return seq

def rnatransl(a):
    seq = ''
    spis = []
    c = len(a)
    for i in range (c//3):
        spis.append(a[3*i - 3:3*i])
    for i in spis:
        if i == 'aug':
           seq += 'Met(START)'
        elif i[0] == 'g' and i[1] == 'g':
            seq += 'Gly'
        elif i[0] == 'g' and i[1] == 'u':
            seq += 'Val'
        elif i[0] == 'g' and i[1] == 'c':
            seq += 'Ala'
        elif i == 'gau' or i == 'gac':
            seq += 'Asp'
        elif i[0] == 'gaa' and i[1] == 'gag':
            seq += 'Glu'
        elif i[0:2] == 'ac':
            seq += 'Thr'
        elif i[0:2] == 'au' and i[-1] != 'g':
            seq += 'Ile'
        elif i == 'aag' or i == 'aaa':
            seq += 'Lys'
        elif i == 'aac' or i == 'aau':
            seq += 'Asn'
        elif i == 'agg' or i == 'aga':
            seq += 'Arg'
        elif i == 'agc' or i == 'agu':
            seq += 'Ser'
        elif i[0:2] == 'cg':
            seq += 'Arg'
        elif i[0:2] == 'cc':
            seq += 'Pro'
        elif i[0:2] == 'cu':
            seq += 'Leu'
        elif i == 'cac' or i == 'cau':
            seq += 'His'
        elif i == 'cag' or i == 'caa':
            seq += 'Gln'
        elif i[0:2] == 'uc':
            seq += 'Ser'
        elif i == 'uuu' or i == 'uuc':
            seq += 'Phe'
        elif i == 'uua' or i == 'uug':
            seq += 'Leu'
        elif i == 'uau' or i == 'uac':
            seq += 'Tyr'
        elif i == 'ugu' or i == 'ugc':
            seq += 'Cys'
        elif i == 'ugg':
           seq += 'trp'
        elif i == 'uaa' or i == 'uag' or i == 'uga':
            seq += '(STOP)'



def handle_dialog(req, res):
    global q
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "рнк",
                "а что это такое?",
                "днк",

            ]
        }
        res['response']['text'] = 'Привет!Выбирай!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in ['а что это такое?']:
        sessionStorage[user_id] = {
            'suggests': [
                "рнк",
                "днк",
            ]
        }
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Более подробно можно прочитать тут: https://scienceland.info/biology10/dna-rna'
        res['response']['card']['image_id'] = "1030494/7ba58d3ea3f05f2fd909"
        res['response']['text'] = 'А теперь выбирай!'
        res['response']['buttons'] = get_suggests(user_id)

        return

    if req['request']['original_utterance'].lower() in ['рнк','rna']:
        sessionStorage[user_id] = {
            'suggests': [
                "трансляция",
                "обратная транскрипция"

            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return



    if req['request']['original_utterance'].lower() in ['трансляция']:
        res['response']['text'] = 'Вводи последовательность РНК(язык не важен)'
        q = 1
        return

    if req['request']['original_utterance'].lower() in ['днк','dna']:
        res['response']['text'] = 'Вводи последовательность ДНК(язык не важен)'
        q = 2
        return

    if req['request']['original_utterance'].lower() in ['обратная транскрипция']:
        res['response']['text'] = 'Вводи последовательность РНК(язык не важен)'
        q = 3
        return

    if  q == 1:
        a = req['request']['original_utterance']
        res['response']['text'] = rnatransl(a)
        res['response']['end_session'] = True
        return

    if  q == 2:
        a = req['request']['original_utterance']
        res['response']['text'] = dnatransk(a)
        res['response']['end_session'] = True
        return

    if  q == 3:
        a = req['request']['original_utterance']
        res['response']['text'] = rnarevtransk(a)
        res['response']['end_session'] = True
        return




def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:3]
    ]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    return suggests

if __name__ == '__main__':
    app.run()