import mysql.connector
from app.settings import DATABASE

class ContactAanvraag:
    def __init__(self, id=None, naam=None, email=None, onderwerp=None, bericht=None):
        self.id = id
        self.naam = naam
        self.email = email
        self.onderwerp = onderwerp
        self.bericht = bericht

    def opslaan(self):
        conn = mysql.connector.connect(**DATABASE)
        cursor = conn.cursor()

        #query om de aanvraag op te slaan
        query = """
            INSERT INTO contact_aanvragen (naam, email, onderwerp, bericht)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (self.naam, self.email, self.onderwerp, self.bericht))
        conn.commit() #slaat de ingevulde variable op in de database

        cursor.close() 
        conn.close() #sluit de verbinding met de database af
