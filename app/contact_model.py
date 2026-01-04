from app.database import get_db_connection

class ContactAanvraag:
    repo = True  #geeft aan dat deze class database-logica bevat

    def __init__(self, id=None, naam=None, email=None, onderwerp=None, bericht=None, antwoord=None, status=None, datum_ingediend=None):
        self.id = id
        self.naam = naam
        self.email = email
        self.onderwerp = onderwerp
        self.bericht = bericht
        self.antwoord = antwoord
        self.status = status
        self.datum_ingediend = datum_ingediend

    def opslaan(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        #query om de aanvraag op te slaan
        query = """
            INSERT INTO contact_aanvragen (naam, email, onderwerp, bericht)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (self.naam, self.email, self.onderwerp, self.bericht))

        conn.commit() #slaat de ingevulde variable op in de database
        cursor.close()
        conn.close()  #sluit de verbinding met de database af

    @staticmethod
    def get_open_vragen():
        #maakt verbinding met de database
        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        #query om alle vragen zonder antwoord op te halen
        query = """
            SELECT * FROM contact_aanvragen
            WHERE antwoord IS NULL
        """
        cursor.execute(query)

        rows = cursor.fetchall()  #haalt alle resultaten op

        cursor.close()
        conn.close()  #sluit de databaseverbinding

        #zet elke database rij om in een ContactAanvraag object
        return [ContactAanvraag(**row) for row in rows]

    @staticmethod
    def beantwoord(vraag_id, antwoord):
        #maakt verbinding met de database
        conn = get_db_connection()
        cursor = conn.cursor()

        #query om een vraag te beantwoorden
        query = """
            UPDATE contact_aanvragen
            SET antwoord = %s
            WHERE id = %s
        """
        cursor.execute(query, (antwoord, vraag_id))

        conn.commit()  #slaat het antwoord op in de database
        cursor.close()
        conn.close()  #sluit de databaseverbinding

    @staticmethod
    def get_by_id(vraag_id): #haalt specifieke id op die wordt gekozen
        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM contact_aanvragen WHERE id = %s" #selecteert id in de database
        cursor.execute(query, (vraag_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return ContactAanvraag(**row)
        return None