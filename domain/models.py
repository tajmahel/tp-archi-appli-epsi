from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass(frozen=True)
class Tarification:
    prix_base: int = 10
    
    def calculer(self, est_heure_de_pointe: bool) -> int:
        # Pattern Strategy
        if est_heure_de_pointe:
            return self.prix_base * 2
        return self.prix_base

@dataclass(frozen=True)
class CreneauHoraire:
    debut: datetime
    fin: datetime

    def est_heure_de_pointe(self) -> bool:
        return 14 <= self.debut.hour < 18

@dataclass
class Membre:
    id_membre: str
    nom: str
    credits: int

@dataclass
class Ressource:
    id_ressource: str
    type: str  # 'SALLE', 'VIDEOPROJECTEUR'
    nom: str

class Reservation:
    def __init__(self, res_id, membre, ressource, creneau):
        self.id = res_id
        self.membre = membre
        self.ressource = ressource
        self.creneau = creneau
        self.statut = "VALIDEE"
        self.tarificateur = Tarification()

    def obtenir_prix_final(self) -> int:
        return self.tarificateur.calculer(self.creneau.est_heure_de_pointe())

    def annuler(self) -> str:
        delai = self.creneau.debut - datetime.now()
        if delai > timedelta(hours=48):
            return "REMBOURSEMENT_100"
        elif delai > timedelta(hours=24):
            return "REMBOURSEMENT_50"
        return "AUCUN_REMBOURSEMENT"