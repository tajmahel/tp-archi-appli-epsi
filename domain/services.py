class ReservationService:
    @staticmethod
    # RÈGLE MÉTIER : Un vidéoprojecteur nécessite une salle sur le même créneau
    def verifier_dependance_materiel(type_ressource, creneau, reservations_existantes):
        if type_ressource not in ["VIDEOPROJECTEUR", "SALLE"]:
            raise ValueError("Réservation impossible : Ressource inconnue")
        if type_ressource == "VIDEOPROJECTEUR":
            a_une_salle = any(
                r.ressource.type == "SALLE" and r.creneau == creneau 
                for r in reservations_existantes
            )
            if not a_une_salle:
                raise ValueError("Réservation impossible : Vidéoprojecteur sans salle.")