import sqlite3

class ReservationRepository:
    def __init__(self, db_path="coworking.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS reservations 
                         (id TEXT PRIMARY KEY, membre_id TEXT, ressource_id TEXT, debut TEXT)""")

    def sauvegarder(self, reservation):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO reservations VALUES (?, ?, ?, ?)",
                         (reservation.id, reservation.membre.id_membre, 
                          reservation.ressource.id_ressource, reservation.creneau.debut.isoformat()))