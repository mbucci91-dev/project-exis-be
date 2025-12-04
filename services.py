from models import User, Card, Movement
from keys import *
from exceptions import ResourceNotFound, PermissionDenied, AuthenticationError
from flask_jwt_extended import create_access_token, decode_token
from cryptography.fernet import Fernet
import random

USER_NOT_FOUND = "L'utente richiesto non è presente nel sistema."
CARD_NOT_FOUND = "La carta richiesta non esiste o è stata rimossa."
CARD_NO_ACTIVE = "La carta non è attiva. Impossibile visualizzare i movimenti."
LOGIN_FAILED = "Credenziali non valide. Riprova."
USER_BLOCKED = "Utente bloccato. Contattare l'assistenza."
FORBIDDEN_ACCESS = "Accesso negato. Risorsa non disponibile o non autorizzata."
INVALID_OWNER_TOKEN_CHALLENGE = "Il token challenge non appartiene a questo utente."
INVALID_TOKEN_CHALLENGE = "Token challenge non valido o scaduto."
TWO_DIGITS_ERROR = "Devi fornire esattamente 2 cifre."
INCORRECT_PIN = "Le cifre del PIN inserite non sono corrette."
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
            "cvv_masked": "***",
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

def create_pin_challenge(user_id):

    indices = random.sample(range(0, 5), 2)
    
    challenge_data = {"req_indices": indices}
    
    challenge_token = create_access_token(
        identity=str(user_id), 
        additional_claims=challenge_data, 
        expires_delta=False
    )
    
    human_indices = [i + 1 for i in indices]
    
    return {
        "indices_to_ask": human_indices,
        "challenge_token": challenge_token
    }

def verify_challenge_and_execute(user_id, digits_input, challenge_token, action_callback):

    try:
        decoded = decode_token(challenge_token)
        if str(decoded['sub']) != str(user_id):
             raise PermissionDenied(INVALID_OWNER_TOKEN_CHALLENGE)
             
        required_indices = decoded['req_indices']
    except Exception:
        raise PermissionDenied(INVALID_TOKEN_CHALLENGE)

    user = User.query.get(user_id)
    if not user: raise ResourceNotFound(USER_NOT_FOUND)

    if len(digits_input) != 2:
        raise PermissionDenied(TWO_DIGITS_ERROR)

    real_pin = user.secret_pin
    
    val_1 = digits_input[0]
    expected_1 = real_pin[required_indices[0]]
    
    val_2 = digits_input[1]
    expected_2 = real_pin[required_indices[1]]
    
    if str(val_1) != str(expected_1) or str(val_2) != str(expected_2):
        raise PermissionDenied(INCORRECT_PIN)

    return action_callback()

def _logic_block_card(user_id, card_id):

    card = Card.query.get(card_id)
    if not card: raise ResourceNotFound(CARD_NOT_FOUND)
    if card.user_id != user_id: raise PermissionDenied(FORBIDDEN_ACCESS)
    
    if card.status == S_CARD_BLOCKED:
        return {"status": "Carta già bloccata", "new_status": S_CARD_BLOCKED}

    card.status = S_CARD_BLOCKED
    from models import db
    db.session.commit()
    return {"status": "Carta bloccata", "new_status": S_CARD_BLOCKED}


def _logic_show_details(user_id, card_id):
    
    card = Card.query.get(card_id)
    if not card: raise ResourceNotFound(CARD_NOT_FOUND)
    if card.user_id != user_id: raise PermissionDenied(FORBIDDEN_ACCESS)

    if card.status != S_CARD_ACTIVE:
        raise PermissionDenied("Impossibile mostrare i dati: la carta non è attiva.")

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    encrypted_pan = cipher_suite.encrypt(card.pan.encode()).decode()
    
    encrypted_cvv = cipher_suite.encrypt(card.cvv.encode()).decode()

    return {
        "temp_key": key.decode(),
        "encrypted_data": { 
            KEY_PAN: encrypted_pan, 
            KEY_CVV: encrypted_cvv 
        }
    }