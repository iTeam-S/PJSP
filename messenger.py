import requests
from conf import BASE_URL
class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    def send_message(self, dest_id, message, prio=False):
        self.send_action(dest_id, 'typing_on')
        """
            Cette fonction sert à envoyer une message texte
                à un utilisateur donnée
        """
        data_json = {
            'recipient': {
                "id": dest_id
            },
            'message': {
                "text": message
            }
        }
        if prio:
            data_json["messaging_type"] = "MESSAGE_TAG"
            data_json["tag"] = "ACCOUNT_UPDATE"

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        self.send_action(dest_id, 'typing_off')
        return res

    def send_action(self, dest_id, action):
        """
            Cette fonction sert à simuler un action sur les messages.
            exemple: vue, en train d'ecrire.
            Action dispo: ['mark_seen', 'typing_on', 'typing_off']
        """

        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },
            'sender_action': action
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )

    def send_quick_reply(self, dest_id, **kwargs):
        '''
            Envoie des quick reply messenger
        '''
        if kwargs.get('MENU_PRINCIPALE'):
            text = "Bienvenue sur le projet Tomady☺"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Soldes",
                    "payload": "_SOLDE",
                    "image_url": f"{BASE_URL}/icons/solde.png"
                },
                {
                    "content_type": "text",
                    "title": "Pensions",
                    "payload": "_PENSION",
                    "image_url":f"{BASE_URL}/icons/pension.png"
                },

                {
                    "content_type": "text",
                    "title": "PJSP",
                    "payload": "_APP",
                    "image_url": f"{BASE_URL}/icons/pjsp.png"
                }
            ] 
        else:
            return


        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },
            'message': {
                'text': text,
                'quick_replies': quick_rep[:13]
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )

    def send_result(self, destId, elements, **kwargs):
        '''
            Affichage de resultat de façon structuré
            chez l'utilisateur
        '''

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements,
                    },
                },
            }
        }

        if kwargs.get("next"):
            dataJSON['message']['quick_replies'] = kwargs.get("next")

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages', json=dataJSON,
            headers=header, params=params
        )


    def send_button(self, destId,title, elements):
        '''
            Affichage de resultat de façon structuré
            chez l'utilisateur
        '''

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":title,
                    "buttons":elements
                    }
                }
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        return requests.post(
            self.url + '/messages', json=dataJSON,
            headers=header, params=params
        )


    def send_file_url(self, destId, url, filetype='file'):
        '''
            Envoyé piece jointe par lien.
        '''

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                'attachment': {
                    'type': filetype,
                    'payload': {
                        "url": url,
                        "is_reusable": True
                    }
                }
            }
        }
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        return requests.post(
            self.url + '/messages',
            json=dataJSON,
            headers=header,
            params=params
        )

 