import mysql.connector
from conf import DATABASE

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
            response["data"].append(res)
            lastID = res[0]
        response["init"] = lastID

        return response

    def _close(self):
        self.db.close()

req = Requete()
req.getListeMenu(1,0)
    