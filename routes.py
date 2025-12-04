from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from keys import *
import services
from exceptions import ResourceNotFound, PermissionDenied, AuthenticationError

api = Blueprint('api', __name__)

GENERIC_ERROR = "Errore generico"

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