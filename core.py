import requete
import messenger
from conf import ACCESS_TOKEN ,BASE_URL
req = requete.Requete()

# Instanciation du Bot Messenger
bot = messenger.Messenger(ACCESS_TOKEN)

class Traitement:

    #  ************************** OPTIONS *******************************

    def __execution(self, user_id, commande):
        '''
            Fonction privée qui traite les differentes commandes réçu
        '''
        bot.send_action(user_id,'mark_seen')


    
    def _analyse(self, data):
        '''
            Fonction analysant les données reçu de Facebook
            Donnée de type Dictionnaire attendu (JSON parsé)
        '''
    
        for event in data['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # recuperation de l'id de l'utilisateur
                    sender_id = message['sender']['id']
                    req.verifUtilisateur(sender_id) 
                    if message['message'].get('attachments'):
                        # recuperations des fichiers envoyés.
                        data = message['message'].get('attachments')
                        # data[0]['type'] == 'file'
                        self.__execution(
                            sender_id,
                            data[0]['payload']['url']
                        )
                    elif message['message'].get('attachments'):
                        # recuperations des fichiers envoyés.
                        data = message['message'].get('attachments')
                        # data[0]['type'] == 'file'
                        self.__execution(
                            sender_id,
                            data[0]['payload']['url']
                        )
                    elif message['message'].get('quick_reply'):
                        # cas d'une reponse de type QUICK_REPLY
                        self.__execution(
                            sender_id,
                            message['message']['quick_reply'].get('payload')
                        )

                    elif message['message'].get('text'):
                        # cas d'une reponse par text simple.
                        self.__execution(
                            sender_id,
                            message['message'].get('text')
                        )
                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    pst_payload = message['postback']['payload']
                    # envoie au traitement
                    self.__execution(recipient_id, pst_payload)
    