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