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

    def _close(self):
        self.db.close()
