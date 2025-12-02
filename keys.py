# --- UTENTE ---
TABLE_USER = "user"
KEY_USER_ID = "id"
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_STATUS = "status"

# Valori Stato Utente
S_USER_ACTIVE = "Active"
S_USER_BLOCKED = "Blocked"

# --- CARTA ---
TABLE_CARD = "card"
KEY_CARD_ID = "id"
KEY_PAN = "pan"
KEY_HOLDER = "holder"
KEY_EXP_DATE = "exp_date"
KEY_USER_ID_FK = "user_id"

# Valori Stato Carta
S_CARD_ACTIVE = "active"
S_CARD_BLOCKED = "blocked"
S_CARD_IN_ACTIVATION = "in activation"

# --- MOVIMENTO ---
TABLE_MOVEMENT = "movement"
KEY_MOV_ID = "id"
KEY_DATE = "date"
KEY_AMOUNT = "amount"
KEY_DESCRIPTION = "description"
KEY_CARD_ID_FK = "card_id"