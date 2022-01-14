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
        self.cursor = self.db.cursor(buffered=True)
    

    def verif_db(fonction):
        '''
            Un decorateur de verification de la
            connexion au serveur avant traitement.
        '''
        def trt_verif(*arg, **kwarg):
            if not arg[0].db.is_connected():
                # reconnexion de la base
                try:
                    arg[0].db.reconnect()
                except Exception:
                    arg[0].__connect()
            return fonction(*arg, **kwarg)
        return trt_verif

    @verif_db
    def verifUtilisateur(self, userID):
        req = '''
		    INSERT IGNORE INTO Utilisateur 
		    (id) VALUES (%s)
		'''
        self.cursor.execute(req, (userID,))
        self.db.commit()

    @verif_db
    def getStatus(self, userID):
        req = '''
		    SELECT status FROM Utilisateur WHERE id = %s
		'''
        self.cursor.execute(req, (userID,))

        return self.cursor.fetchone()[0]

    @verif_db
    def setStatus(self, userID, action):
        req = '''
			UPDATE Utilisateur set status = %s
			WHERE id = %s
		'''
        self.cursor.execute(req, (action, userID))
        self.db.commit()

    @verif_db
    def getLastTypeDocument (self , type):
        req = """
            SELECT MAX(n_nature)
            FROM nature
            WHERE n_typedocument = %s 
        """
        self.cursor.execute(req,(type,))
        return self.cursor.fetchone()[0]

    @verif_db
    def getListeMenu(self, type, init=0):
        """
            Récuperer la liste des nature,
            en passe en paramètre :
                Le type de paramètre :
                    1 ===> Pour solde
                    2 ===> Pour les pensions
                Init : 
                    L'ID de la dernière donnée envoyé afin 
                    de gérer le système de next
        """
        
        if type == 1:
            subtitle = "Solde"
            image = f"{BASE_URL}/icons/solde_photo.jpg"
        else :
            subtitle = "Pension"
            image = f"{BASE_URL}/icons/pension_photo.jpg"
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
            title = str(res[1]).replace('\n','')
            title = str(title).replace('\r','')
            title = str(title).replace('\t','')
            response["data"].append({
                        'title': title,
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
                                "payload": f"_SHOW_INFO_{subtitle.upper()}_{res[0]}"
                            }
                        ]
                    })
            lastID = res[0]                  
        response["lastID"] = int(lastID)

        len = int(self.getLastTypeDocument(type))
        if lastID < len : next = True 
        else :next = False
        response["next"]=next
        return response

    @verif_db
    def searchListMenu(self, query, init=0):
        """
            Recherche la liste des nature,

        """

        template = f"%{query}%"
        req = '''
            SELECT n_nature , libelle_nature ,n_typedocument
            FROM nature
            WHERE n_nature > %s AND LOWER(nature.libelle_nature) LIKE %s
            ORDER BY n_nature 
            LIMIT 10
        '''
        self.cursor.execute(req,(init,template))
        resultat = self.cursor.fetchall()
        response = {}
        response["data"] = []
        for res in resultat :
            if res[2] == 1:
                subtitle = "Solde"
                image = f"{BASE_URL}/icons/solde_photo.png"
            else :
                subtitle = "Pension"
                image = f"{BASE_URL}/icons/pension_photo.jpeg"
            title = str(res[1]).replace('\n','')
            title = str(title).replace('\r','')
            title = str(title).replace('\t','')
            response["data"].append({
                        'title': title,
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
                                "payload": f"_SHOW_INFO_{subtitle.upper()}_{res[0]}"
                            }
                        ]
                    })
        return response

    @verif_db
    def getReferenceNature(self,ID):
        req = """
            SELECT n_article, text_article 
            FROM article 
            WHERE id_nature=%s
        """
        self.cursor.execute(req,(ID,))
        data = self.cursor.fetchall()
        res = "Réference :"
        for a in data :
            res = res + f"\n -{a[1]} "
        return res

    @verif_db
    def getDetailNature(self,ID,type=1):
        """
            Type =
                1 -> Visa
                2 -> Mandatement
        """
        req = """
            SELECT T.titre , S.sous_titre , P.piece 
            FROM piece P 
            LEFT JOIN sous_titre S ON P.n_soustitre = S.n_soustitre
            LEFT JOIN titre T ON T.n_titre = S.n_titre
            LEFT JOIN nature N ON N.n_nature = T.n_nature
            LEFT JOIN typepiece TP ON TP.n_typepiece = T.n_typepiece
            WHERE N.n_nature = %s 
            AND TP.n_typepiece = %s
            ORDER BY S.sous_titre
        """
        self.cursor.execute(req,(ID,type))
        output= self.cursor.fetchall()   
        res = ""

        current_titre = ""
        current_sous_titre = ""

        for data in output :
            if data[0]!='vide':
                if data[0] != current_titre :
                    current_titre = data[0]
                    res += f"   {data[0]}\n"  
            if data[1]!='vide' :
                if data[1] != current_sous_titre :
                    current_sous_titre = data[1]
                    res += f"   {data[1]} :\n" 
            piece = str(data[2]).replace("\n","")
            piece = str(piece).replace("\t","")
            piece = str(piece).replace("\r","")
            res += f"-{piece}\n"                         
        if res == "" :
            return "Il n'y a pas assez information."
        return res

    def _close(self):
        self.db.close()
