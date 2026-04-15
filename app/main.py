from fastapi import FastAPI, HTTPException
from domain.models import Membre, Ressource, CreneauHoraire, Reservation
from domain.services import ReservationService
from infra.repository import ReservationRepository
from datetime import datetime, timedelta

app = FastAPI()
repo = ReservationRepository()

@app.post("/reserver")
async def api_reserver(m_id: str, res_type: str, heures_dans_futur: int):
    membre = Membre(id_membre=m_id, nom="Utilisateur Test", credits=100)
    
    ressource = Ressource(id_ressource="R1", type=res_type, nom="Espace Alpha")
    debut = datetime.now() + timedelta(hours=heures_dans_futur)
    creneau = CreneauHoraire(debut=debut, fin=debut + timedelta(hours=2))
    
    try:
        ReservationService.verifier_dependance_materiel(res_type, creneau, [])
        
        resa = Reservation(res_id="RESA-" + m_id, membre=membre, ressource=ressource, creneau=creneau)
        cout = resa.obtenir_prix_final()
        
        if membre.credits < cout:
            raise HTTPException(status_code=400, detail=f"Crédits insuffisants. Requis: {cout}, Dispo: {membre.credits}")
        
        repo.sauvegarder(resa)
        
        return {
            "status": "success",
            "reservation_id": resa.id,
            "cout_facture": cout,
            "solde_restant": membre.credits - cout,
            "details": {
                "type": res_type,
                "heure_pointe": creneau.est_heure_de_pointe()
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))