from models import User, Card, Movement
from keys import *
from exceptions import ResourceNotFound, PermissionDenied, AuthenticationError
from flask_jwt_extended import create_access_token

USER_NOT_FOUND = "L'utente richiesto non è presente nel sistema."
CARD_NOT_FOUND = "La carta richiesta non esiste o è stata rimossa."
CARD_NO_ACTIVE = "La carta non è attiva. Impossibile visualizzare i movimenti."
LOGIN_FAILED = "Credenziali non valide. Riprova."
USER_BLOCKED = "Utente bloccato. Contattare l'assistenza."
FORBIDDEN_ACCESS = "Accesso negato. Risorsa non disponibile o non autorizzata."
GENERIC_ERROR = "Si è verificato un errore imprevisto."

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        raise AuthenticationError(LOGIN_FAILED)

    if user.status == S_USER_BLOCKED:
        raise PermissionDenied(USER_BLOCKED)

    access_token = create_access_token(identity=str(user.id))
    
    return {
        "token": access_token,
        KEY_USERNAME: user.username,
        KEY_STATUS: user.status
    }

def get_user_cards(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ResourceNotFound(USER_NOT_FOUND)

    cards = Card.query.filter_by(user_id=user_id).all()
    
    results = []
    for card in cards:
        results.append({
            KEY_CARD_ID: card.id,
            "pan_masked": f"**** **** **** {card.pan[-4:]}",
            KEY_HOLDER: card.holder,
            KEY_EXP_DATE: card.exp_date,
            KEY_STATUS: card.status
        })
    return results

def get_card_movements(user_id, card_id):
    card = Card.query.get(card_id)
    
    if not card:
        raise ResourceNotFound(CARD_NOT_FOUND)
    
    if card.user_id != user_id:
        raise PermissionDenied(FORBIDDEN_ACCESS)

    if card.status != S_CARD_ACTIVE:
        raise PermissionDenied(CARD_NO_ACTIVE)

    movements = Movement.query.filter_by(card_id=card_id).order_by(Movement.date.desc()).all()
    
    results = []
    for mov in movements:
        results.append({
            KEY_MOV_ID: mov.id,
            KEY_DATE: mov.date.strftime('%d/%m/%Y'),
            KEY_AMOUNT: mov.amount,
            KEY_DESCRIPTION: mov.description
        })
    return results