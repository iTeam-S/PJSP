import core
from threading import Thread
from conf import VERIFY_TOKEN
from flask import Flask, request,send_from_directory, abort

traitement = core.Traitement()
# Instanciation du serveur web
webserver = Flask(__name__)

@webserver.route("/", methods=["GET", "POST"])
def receive_message():
    if request.method == "GET":
        '''
            C'est seuelement dans le cas ou facebook va vérifier l'état du serveur Webhook.
        '''
        token_sent = request.args.get("hub.verify_token")
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
    elif request.method == "POST":
        '''
            Les requetes envoyés en moode 'POST' sont les messages
            envoyé sur la page Facebook et qui sont à traiter.
        '''
        body = request.get_json()
        if not request.args.get("TEST"):
            # Traitement du process dans un autre Thread.
            '''
                Empeche la reponse timeout du requete de Facebook
                au cas ou la demande est longue à traiter.
            '''
            proc = Thread(target=traitement._analyse, args=[body])
            proc.start()
        else:
            # La requete attend la finition du traitement
            '''
                Dans ce cas, la requete est une simulation lancé
                par un des test unitaires ou fonctionnels configuré.
            '''
            traitement._analyse(body)
    return "receive", 200
@webserver.route("/assets/<filename>", methods=["GET"])
def get_file(filename):
    try:
        return send_from_directory(
                    './assets/',
                    path=filename,
                    as_attachment=True
                )
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    # Lancement du serveur web
    webserver.run(port=8071)