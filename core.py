from requests.api import request
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
        bot.persistent_menu(user_id)
        bot.send_action(user_id,'mark_seen')
        
        status = req.getStatus(user_id)
        if commande.startswith('_PAGE_SOLDE_') :
            lastID = int(commande.replace('_PAGE_SOLDE_',''))
            data = req.getListeMenu(1,lastID)
            if data["next"] == True :
                lastID = data["lastID"]
                next = [
                        {
                            "content_type": "text",
                            "title":"Next",
                            "payload": f"_PAGE_SOLDE_{lastID}",
                            "image_url":f"{BASE_URL}/icons/next.png"
                        }
                    ]
                bot.send_result(user_id, data["data"],next= next)
            else :
                bot.send_result(user_id, data["data"])
            return

        elif commande == '_MAIN' :
            bot.send_quick_reply(user_id, MENU_PRINCIPALE=True)
            return 

        elif commande.startswith('_PAGE_PENSION_') :
            lastID = int(commande.replace('_PAGE_PENSION_',''))
            data = req.getListeMenu(2,lastID)
            if data["next"] == True :
                lastID = data["lastID"]
                next = [
                        {
                            "content_type": "text",
                            "title":"Next",
                            "payload": f"_PAGE_PENSION_{lastID}",
                            "image_url":f"{BASE_URL}/icons/next.png"
                        }
                    ]
                bot.send_result(user_id, data["data"],next= next)
            else :
                bot.send_result(user_id, data["data"])
            return

        elif commande.startswith('_SHOW_INFO_SOLDE_'):
            ID = commande.replace('_SHOW_INFO_SOLDE_','')
            bot.send_quick_reply(user_id,MENU_SOLDE=True,ID=ID)
            return

        elif commande.startswith('_SHOW_INFO_PENSION_'):
            ID = commande.replace('_SHOW_INFO_PENSION_','')
            bot.send_quick_reply(user_id,MENU_PENSION=True,ID=ID)
            return

        elif commande == 'MENU_PJSP':
            bot.send_quick_reply(user_id,MENU_PJSP=True)
            return

        elif commande == '_MENU_CONTACT':
            bot.send_quick_reply(user_id,MENU_CONTACT=True)
            return
        
        elif commande == '_DOWNLOAD' :
            bot.send_message(user_id, "Attendez un peu , on est en train de le télecharger.")
            bot.send_file_url(user_id, f"{BASE_URL}/icons/pjsp.apk")
            return
        elif commande == 'GET_STARTED':
            bot.persistent_menu(user_id)
            return

        elif commande == '_SEARCH' or  commande == '_SEARCH_OUI':
            bot.send_message(user_id, "Veuillez saisir votre mot clé (>3 caractères).")
            req.setStatus(user_id,"_attente_query")
            return  
        elif commande== '_SEARCH_NON':
            req.setStatus(user_id,"")
            return          

        elif commande.startswith('_SOLDE'):
            commande = commande.replace('_SOLDE','')
            if commande.startswith('_REF_'):
                commande = commande.replace('_REF_','')
                ID = int(commande)
                detail = req.getReferenceNature(ID)
                bot.send_message(user_id,detail)
                return

            elif commande.startswith('_VISA_'):
                commande = commande.replace('_VISA_','')
                ID = int(commande)
                detail = req.getDetailNature(ID,1)
                bot.send_message(user_id,detail)
                return

            elif commande.startswith('_MDT_'):
                commande = commande.replace('_MDT_','')
                ID = int(commande)
                detail = req.getDetailNature(ID,2)
                bot.send_message(user_id,detail)
                return

        elif commande.startswith('_PENSION'):
            commande = commande.replace('_PENSION','')
            if commande.startswith('_REF_'):
                commande = commande.replace('_REF_','')
                ID = int(commande)
                detail = req.getReferenceNature(ID)
                bot.send_message(user_id,detail)
                return
            elif commande.startswith('_LQD_'):
                commande = commande.replace('_LQD_','')
                ID = int(commande)
                detail = req.getDetailNature(ID,1)
                bot.send_message(user_id,detail)
                return
        
        elif status == "_attente_query" :
            if len(commande)<3:
                bot.send_quick_reply(user_id,MENU_SEARCH=True)
                req.setStatus(user_id,"")
                return
            else :
                data = req.searchListMenu(commande)
                if len(data["data"]) == 0:
                    bot.send_message(user_id,"Il n'y malheureusement pas de resultats.")
                    bot.send_quick_reply(user_id,MENU_SEARCH=True)
                else :
                    bot.send_message(user_id,"Voici les resultats.")
                    bot.send_result(user_id, data["data"])
                    bot.send_quick_reply(user_id,MENU_SEARCH=True)
                req.setStatus(user_id,"")
                return
        elif commande == "_MENU_PRINCIPAL" :
            req.setStatus(user_id,"")
            bot.send_quick_reply(user_id,MENU_PRINCIPALE=True)
            return

        req.setStatus(user_id,"")
        bot.send_quick_reply(user_id,MENU_PRINCIPALE=True)
    
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
    