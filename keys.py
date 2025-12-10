# --- UTENTE ---
TABLE_USER = "user"
KEY_USER_ID = "id"
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_STATUS = "status"
KEY_EMAIL = "email"
KEY_DOB = "dob"          # Date of Birth
KEY_PHONE = "phone"
KEY_ADDRESS = "address"

# Valori Stato Utente
S_USER_ACTIVE = "Active"
S_USER_BLOCKED = "Blocked"

# --- CARTA ---
TABLE_CARD = "card"
KEY_CARD_ID = "id"
KEY_PAN = "pan"
KEY_HOLDER = "holder"
KEY_CIRCUIT = "circuit"
KEY_EXP_DATE = "exp_date"
KEY_USER_ID_FK = "user_id"
KEY_CVV = "cvv"
KEY_SECRET_PIN = "secret_pin"

# Valori Stato Carta
S_CARD_ACTIVE = "active"
S_CARD_BLOCKED = "blocked"
S_CARD_IN_ACTIVATION = "in activation"

# Valori Circuiti
C_VISA = "Visa"
C_MASTERCARD = "Mastercard"
C_AMEX = "Amex"

# --- MOVIMENTO ---
TABLE_MOVEMENT = "movement"
KEY_MOV_ID = "id"
KEY_DATE = "date"
KEY_AMOUNT = "amount"
KEY_DESCRIPTION = "description"
KEY_CARD_ID_FK = "card_id"