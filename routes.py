from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from keys import *
import services
from exceptions import ResourceNotFound, PermissionDenied, AuthenticationError

api = Blueprint('api', __name__)

GENERIC_ERROR = "Errore generico"
NO_DIGITS_ERROR = "Mancano le cifre del PIN o il token challenge."

def create_response(data=None, code=200, error_key=None):
    if code == 200:
        return jsonify({"message": "Success", "code": 200, "response": data}), 200
    else:
        
        msg = str(error_key) if error_key else GENERIC_ERROR
        return jsonify({"message": msg, "code": code, "response": None}), code


@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data: return create_response(code=400, error_key="Dati mancanti")

        username = data.get(KEY_USERNAME)
        password = data.get(KEY_PASSWORD)

        result = services.authenticate_user(username, password)
        
        return create_response(data=result, code=200)

    except AuthenticationError as e:
        return create_response(code=401, error_key=str(e))
    except PermissionDenied as e:
        return create_response(code=403, error_key=str(e))
    except Exception as e:
        return create_response(code=500, error_key=GENERIC_ERROR)


@api.route('/cards', methods=['GET'])
@jwt_required()
def get_cards():
    try:
        current_user_id = int(get_jwt_identity())
        
        result = services.get_user_cards(current_user_id)
        
        return create_response(data=result, code=200)

    except ResourceNotFound as e:
        return create_response(code=404, error_key=str(e))
    except Exception as e:
        print(e)
        return create_response(code=500, error_key=GENERIC_ERROR)


@api.route('/movements/<int:card_id>', methods=['GET'])
@jwt_required()
def get_movements(card_id):
    try:
        current_user_id = int(get_jwt_identity())

        result = services.get_card_movements(current_user_id, card_id)
        
        return create_response(data=result, code=200)

    except ResourceNotFound as e:
        return create_response(code=404, error_key=str(e))
    except PermissionDenied as e:
        return create_response(code=403, error_key=str(e))
    except Exception as e:
        print(e)
        return create_response(code=500, error_key=GENERIC_ERROR)
    
@api.route('/profile', methods=['GET'])
@jwt_required()
def get_profile_endpoint():
    try:
        current_user_id = int(get_jwt_identity())
        
        result = services.get_user_profile(current_user_id)
        
        return create_response(data=result, code=200)

    except ResourceNotFound as e:
        return create_response(code=404, error_key=str(e))
    except Exception as e:
        print(e)
        return create_response(code=500, error_key=GENERIC_ERROR)
    

@api.route('/auth/challenge', methods=['POST'])
@jwt_required()
def get_challenge():
    try:
        current_user_id = int(get_jwt_identity())
        
        result = services.create_pin_challenge(current_user_id)
        
        return create_response(data=result, code=200)
    except Exception as e:
        return create_response(code=500, error_key=GENERIC_ERROR)


@api.route('/cards/<int:card_id>/block', methods=['POST'])
@jwt_required()
def block_card_endpoint(card_id):
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        digits = data.get('digits')
        token_c = data.get('challenge_token')
        
        if not digits or not token_c:
            return create_response(code=400, error_key=NO_DIGITS_ERROR)

        action_to_do = lambda: services._logic_block_card(current_user_id, card_id)
        
        result = services.verify_challenge_and_execute(current_user_id, digits, token_c, action_to_do)
        
        return create_response(data=result, code=200)

    except PermissionDenied as e:
        return create_response(code=403, error_key=str(e))
    except ResourceNotFound as e:
        return create_response(code=404, error_key=str(e))
    except Exception as e:
        print(e)
        return create_response(code=500, error_key=GENERIC_ERROR)
    
@api.route('/cards/<int:card_id>/details', methods=['POST'])
@jwt_required()
def show_card_details(card_id):
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        digits = data.get('digits')
        token_c = data.get('challenge_token')
        
        if not digits or not token_c:
            return create_response(code=400, error_key=NO_DIGITS_ERROR)

        action_to_do = lambda: services._logic_show_details(current_user_id, card_id)
        
        result = services.verify_challenge_and_execute(current_user_id, digits, token_c, action_to_do)
        
        return create_response(data=result, code=200)

    except PermissionDenied as e:
        return create_response(code=403, error_key=str(e))
    except ResourceNotFound as e:
        return create_response(code=404, error_key=str(e))
    except Exception as e:
        return create_response(code=500, error_key=GENERIC_ERROR)