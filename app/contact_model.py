from app.database import get_db_connection


class ContactAanvraag:
    repo = True

    def __init__(
        self,
        id=None,
        naam=None,
        email=None,
        onderwerp=None,
        bericht=None,
        antwoord=None,
        status=None,
        datum_ingediend=None,
        user_id=None
    ):
        self.id = id
        self.naam = naam
        self.email = email
        self.onderwerp = onderwerp
        self.bericht = bericht
        self.antwoord = antwoord
        self.status = status
        self.datum_ingediend = datum_ingediend
        self.user_id = user_id

    # =========================
    # Ticket opslaan
    # =========================
    def opslaan(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO contact_aanvragen
            (naam, email, onderwerp, bericht, user_id, status)
            VALUES (%s, %s, %s, %s, %s, 'Nieuw')
        """

        cursor.execute(
            query,
            (self.naam, self.email, self.onderwerp, self.bericht, self.user_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

    # =========================
    # Tickets van 1 gebruiker
    # =========================
    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM contact_aanvragen WHERE user_id = %s ORDER BY id DESC",
            (user_id,)
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [ContactAanvraag(**row) for row in rows]

    # =========================
    # Open vragen (admin)
    # =========================
    @staticmethod
    def get_open_vragen():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM contact_aanvragen WHERE antwoord IS NULL"
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [ContactAanvraag(**row) for row in rows]

    # =========================
    # Vraag beantwoorden
    # =========================
    @staticmethod
    def beantwoord(vraag_id, antwoord):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE contact_aanvragen SET antwoord = %s WHERE id = %s",
            (antwoord, vraag_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

    # =========================
    # Ticket ophalen op ID
    # =========================
    @staticmethod
    def get_by_id(vraag_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM contact_aanvragen WHERE id = %s",
            (vraag_id,)
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return ContactAanvraag(**row)
        return None
