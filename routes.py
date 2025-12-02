from flask import Blueprint, jsonify, request
from models import User, Card, Movement
from keys import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

USER_NOT_FOUND = "L'utente richiesto non è presente nel sistema."
CARD_NOT_FOUND = "La carta richiesta non esiste o è stata rimossa."
LOGIN_FAILED = "Credenziali non valide. Riprova."
USER_BLOCKED = "Utente bloccato. Contattare l'assistenza."
FORBIDDEN_ACCESS = "Accesso negato. Risorsa non disponibile o non autorizzata."
GENERIC_ERROR = "Si è verificato un errore imprevisto."

def create_response(data=None, code=200, error_key=None):
    if code == 200:
        message = "Success"
        response_data = data
    else:
        message = error_key
        response_data = None

    return jsonify({
        "message": message,
        "code": code,
        "response": response_data
    }), code


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    req_user = data.get(KEY_USERNAME)
    req_pass = data.get(KEY_PASSWORD)

    if not req_user or not req_pass:
         return create_response(code=400, error_key=GENERIC_ERROR) 

    user = User.query.filter_by(username=req_user).first()

    if user and user.password == req_pass:
        if user.status == S_USER_BLOCKED:
            return create_response(code=403, error_key=USER_BLOCKED)

        access_token = create_access_token(identity=str(user.id))

        return create_response(data={
            "token": access_token,
            KEY_USERNAME: user.username,
            KEY_STATUS: user.status
        }, code=200)
    else:
        return create_response(code=401, error_key=LOGIN_FAILED)


@api.route('/cards', methods=['GET'])
@jwt_required()
def get_cards():
    
    current_user_id = int(get_jwt_identity())
    
    user = User.query.get(current_user_id)
    
    if not user:
        return create_response(code=404, error_key=USER_NOT_FOUND)

    user_cards = Card.query.filter_by(user_id=current_user_id).all()
    
    cards_list = []
    for card in user_cards:
        cards_list.append({
            KEY_CARD_ID: card.id,
            "pan_masked": f"**** **** **** {card.pan[-4:]}",
            KEY_HOLDER: card.holder,
            KEY_EXP_DATE: card.exp_date,
            KEY_STATUS: card.status
        })
    
    return create_response(data=cards_list, code=200)


@api.route('/movements/<int:card_id>', methods=['GET'])
@jwt_required()
def get_movements(card_id):
    current_user_id = int(get_jwt_identity())

    card = Card.query.get(card_id)
    if not card:
        return create_response(code=404, error_key=CARD_NOT_FOUND)
    
    if card.user_id != current_user_id:
        return create_response(code=403, error_key=FORBIDDEN_ACCESS)

    if card.status != S_CARD_ACTIVE:
         return create_response(code=403, error_key=FORBIDDEN_ACCESS)

    movements = Movement.query.filter_by(card_id=card_id).order_by(Movement.date.desc()).all()
    
    mov_list = []
    for mov in movements:
        mov_list.append({
            KEY_MOV_ID: mov.id,
            KEY_DATE: mov.date.strftime('%d/%m/%Y'),
            KEY_AMOUNT: mov.amount,
            KEY_DESCRIPTION: mov.description
        })
        
    return create_response(data=mov_list, code=200)