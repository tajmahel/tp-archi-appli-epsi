# TP Architectures Applicatives - EPSI

**Auteur :** [Ton Nom / Binôme]
**Sujet :** Système de Réservation Co-working (Sujet B)

## Architecture

- **DDD** : Utilisation d'Entités (Membre, Ressource, Reservation) et Value Objects (Creneau, Tarification).
- **SoC** : Séparation stricte entre `app` (FastAPI), `domain` (Règles métier) et `infra` (SQLite).
- **Design Patterns** :
  1. Repository (pour l'accès aux données).
  2. Strategy (pour le calcul dynamique du prix pointe/creuse).

## Lancement

1. `pip install fastapi uvicorn`
2. `uvicorn app.main:app --reload`
3. Tests : `python -m unittest discover tests`

## MEMAIN MAËL