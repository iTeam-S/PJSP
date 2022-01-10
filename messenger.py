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
        '''                # {
                #     "content_type": "text",
                #     "title": "Recherche",
                #     "payload": "_SEARCH",
                #     "image_url": f"{BASE_URL}/icons/search.png"
                # },
        if kwargs.get('MENU_PRINCIPALE'):
            text = "Bienvenue sur PJSP"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Soldes",
                    "payload": "_PAGE_SOLDE_0",
                    "image_url": f"{BASE_URL}/icons/solde.png"
                },
                {
                    "content_type": "text",
                    "title": "Pensions",
                    "payload": "_PAGE_PENSION_0",
                    "image_url":f"{BASE_URL}/icons/pension.png"
                },

                {
                    "content_type": "text",
                    "title": "Recherche",
                    "payload": "_SEARCH",
                    "image_url": f"{BASE_URL}/icons/search.png"
                },

                {
                    "content_type": "text",
                    "title": "PJSP",
                    "payload": "MENU_PJSP",
                    "image_url": f"{BASE_URL}/icons/pjsp.webp"
                },
            ] 
        elif kwargs.get('MENU_SOLDE'):
            text = "Veuillez choisir :"
            ID = kwargs.get('ID')
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Réference",
                    "payload": f"_SOLDE_REF_{ID}",
                    "image_url": f"{BASE_URL}/icons/ref.png"
                },
                {
                    "content_type": "text",
                    "title": "Visa",
                    "payload": f"_SOLDE_VISA_{ID}",
                    "image_url": f"{BASE_URL}/icons/visa.png"
                },
                {
                    "content_type": "text",
                    "title": "Mandatement",
                    "payload": f"_SOLDE_MDT_{ID}",
                    "image_url": f"{BASE_URL}/icons/mdt.png"
                },
            ]

        elif kwargs.get('MENU_PENSION'):
            text = "Veuillez-choisir :"
            ID = kwargs.get('ID')
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Réference",
                    "payload": f"_PENSION_REF_{ID}",
                    "image_url": f"{BASE_URL}/icons/ref.png"
                },
                {
                    "content_type": "text",
                    "title": "Liquidation",
                    "payload": f"_PENSION_LQD_{ID}",
                    "image_url": f"{BASE_URL}/icons/lqd.png"
                },
            ]
        elif kwargs.get('MENU_SEARCH'):
            text = "Voulez-vous ressayez?"
            ID = kwargs.get('ID')
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "✅OUI",
                    "payload": f"_SEARCH_OUI",
                },
                {
                    "content_type": "text",
                    "title": "❌NON",
                    "payload": f"_SEARCH_NON",
                },
            ]
        elif kwargs.get('MENU_PJSP'):
            text = "Veuillez choisir :"
            ID = kwargs.get('ID')
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Contact",
                    "payload": "_MENU_CONTACT",
                    "image_url": f"{BASE_URL}/icons/contact.png"
                },
                {
                    "content_type": "text",
                    "title": "Doléance",
                    "payload": f"_DOLEANCE",
                    "image_url": f"{BASE_URL}/icons/doleance.png"
                },
                {
                    "content_type": "text",
                    "title": "Télecharger",
                    "payload": f"_DOWNLOAD",
                    "image_url": f"{BASE_URL}/icons/download.png"
                },
            ]
        elif kwargs.get('MENU_CONTACT'):
            text = "Veuillez choisir :"
            quick_rep = [
                {
                    "content_type": "text",
                    "title": "Service regional",
                    "payload": f"_PAGE_CONTACT_SERVICE_0",
                    "image_url": f"{BASE_URL}/icons/contact.png"
                },
                {
                    "content_type": "text",
                    "title": "Antenne",
                    "payload": f"_PAGE_CONTACT_ANTENNE_0",
                    "image_url": f"{BASE_URL}/icons/doleance.png"
                },
                {
                    "content_type": "text",
                    "title": "Service centrale",
                    "payload": f"_DOWNLOAD",
                    "image_url": f"{BASE_URL}/icons/download.png"
                },
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

    def persistent_menu(self, destId):
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        dataJSON = {
            "psid": destId,
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": 'false',
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": "🏠Menu principal",
                            "payload": "_MENU_PRINCIPAL"
                        },
                    ]
                }
            ]
        }

        res = requests.post(
            'https://graph.facebook.com/v12.0/me/custom_user_settings',
            json=dataJSON, headers=header, params=params
        )
        return res
