import mysql.connector
from conf import DATABASE, BASE_URL

class Requete:
    def __init__(self):
        '''
            Initialisation: Connexion à la base de données
        '''
        self.__connect()


    def __connect(self):
        self.db = mysql.connector.connect(**DATABASE)
        self.cursor = self.db.cursor()
    

    def __verif(self):
        if not self.db.is_connected():
            self.db.reconnect()



    def verifUtilisateur(self, userID):
        self.__verif()
        req = '''
		    INSERT IGNORE INTO Utilisateur 
		    (id) VALUES (%s)
		'''
        self.cursor.execute(req, (userID,))
        self.db.commit()


    def getStatus(self, userID):
        self.__verif()
        req = '''
		    SELECT status FROM Utilisateur WHERE id = %s
		'''
        self.cursor.execute(req, (userID,))

        return self.cursor.fetchone()[0]

    def setStatus(self, userID, action):
        self.__verif()
        req = '''
			UPDATE Utilisateur set status = %s
			WHERE id = %s
		'''
        self.cursor.execute(req, (action, userID))
        self.db.commit()


    def getLastTypeDocument (self , type):
        self.__verif()
        req = """
            SELECT MAX(n_nature)
            FROM nature
            WHERE n_typedocument = %s 
        """
        self.cursor.execute(req,(type,))
        return self.cursor.fetchone()[0]

    def getListeMenu(self, type, init=0):
        """
            Récuperer la liste des nature,
            en passe en paramètre :
                Le type de paramètre :
                    1 ===> Pour solde
                    2 ===> Pour les documents
                Init : 
                    L'ID de la dernière donnée envoyé afin 
                    de gérer le système de next
        """
        self.__verif()
        
        if type == 1:
            subtitle = "Pension"
            image = f"{BASE_URL}/icons/pension_photo.jpg"
        else :
            subtitle = "Solde"
            image = f"{BASE_URL}/icons/solde_photo.jpg"
        req = '''
            SELECT n_nature , libelle_nature
            FROM nature
            WHERE n_typedocument = %s AND n_nature > %s
            ORDER BY n_nature 
            LIMIT 10
        '''
        self.cursor.execute(req,(type,init))
        resultat = self.cursor.fetchall()

        lastID = 0
        response = {}
        response["data"] = []
        for res in resultat :
            response["data"].append({
                        'title': str(res[1]).replace('\n',''),
                        'subtitle': subtitle,
                        'image_url': image,
                        "default_action": {
                            "type": "web_url",
                            "url": "https://www.mouser.fr/",
                            "webview_height_ratio": "tall",
                            },
                        'buttons': [
                            {
                                "type": "postback",
                                "title": "Plus d'info",
                                "payload": f"_SHOW_INFO_{str(type)}_{res[0]}"
                            }
                        ]
                    })
            lastID = res[0]                  
        response["lasID"] = int(lastID)

        len = int(self.getLastTypeDocument(type))
        if lastID < len : next = True 
        else :next = False
        response["next"]=next
        return response

    def _close(self):
        self.db.close()

req = Requete()
print(req.getListeMenu(1,13))