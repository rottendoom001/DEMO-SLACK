import requests
import json

def handler(event, context):
    URL = 'https://hooks.slack.com/services/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'
    print("EVENT :", event)
    records = event.get('Records', [])
    detail = event.get('detail',{})
    cw_mess = event.get('message','NONE')
    message = ''
    # ALERTA EVENTO PROGRAMADO (TIPO 1)
    if cw_mess != 'NONE':
        message = 'ALERTA PROGRAMADA: ' + cw_mess

    # ALERTA CAMBIO DE ESTADO EC2 (TIPO 2)
    if detail != {} :
        instance = detail.get('instance-id','NO DEFINIDO')
        state = detail.get('state','NO DEFINIDO')
        message = 'ALERTA EN LA INSTANCIA :' + instance + ' ESTADO ACTUAL :' + state

    # ALERTA USO DE CPU EC2 (TIPO3)
    if records != []:
        record = records[0]
        sns = record.get('Sns', {})
        mess = json.loads(sns.get('Message', '{}'))
        print ('Message', message)
        message =  'ALERTA TIPO 3 :' + mess.get('NewStateReason')

    payload = {
        "channel": "#aws-slack-demo",
        "username": "webhookbot",
        "text": message,
        "icon_emoji": ":ghost:"
        }
    requests.post(URL, json=payload)
