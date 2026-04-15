import pytest
from datetime import datetime, timedelta
from domain.models import Reservation, Membre, Ressource, CreneauHoraire
from domain.services import ReservationService

def test_tarification_pointe_stub():
    date_pointe = datetime.now().replace(hour=15, minute=0)
    creneau = CreneauHoraire(date_pointe, date_pointe)
    membre = Membre("M1", "Test", 100)
    ressource = Ressource("S1", "SALLE", "Meeting")
    
    resa = Reservation("ID", membre, ressource, creneau)
    assert resa.obtenir_prix_final() == 20
    
def test_sauvegarde_mock(mocker):
    mock_repo = mocker.Mock()
    mock_resa = mocker.Mock()
    mock_repo.sauvegarder(mock_resa)
    mock_repo.sauvegarder.assert_called_once_with(mock_resa)

def test_reservation_videoprojecteur_sans_salle_doit_echouer():
    date_future = datetime.now() + timedelta(days=1)
    creneau = CreneauHoraire(date_future, date_future + timedelta(hours=2))
    
    with pytest.raises(ValueError) as excinfo:
        ReservationService.verifier_dependance_materiel("VIDEOPROJECTEUR", creneau, [])
    
    assert "Vidéoprojecteur sans salle" in str(excinfo.value)
    
    
def test_annulation_remboursement_50_pourcent():
    # Cas : annulé 30h avant (entre 24 et 48h)
    futur = datetime.now() + timedelta(hours=30)
    creneau = CreneauHoraire(futur, futur + timedelta(hours=1))
    membre = Membre("M1", "Test", 100)
    ressource = Ressource("S1", "SALLE", "Meeting")
    resa = Reservation("R1", membre, ressource, creneau)
    
    assert resa.annuler() == "REMBOURSEMENT_50"

def test_annulation_remboursement_zero():
    # Cas : annulé 5h avant (moins de 24h)
    tres_proche = datetime.now() + timedelta(hours=5)
    creneau = CreneauHoraire(tres_proche, tres_proche + timedelta(hours=1))
    resa = Reservation("R1", Membre("M1", "T", 100), Ressource("S1", "S", "M"), creneau)
    
    assert resa.annuler() == "AUCUN_REMBOURSEMENT"