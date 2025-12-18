# project-exis

# Exis - Backend API (Gestore Carte di Pagamento)

Questo repository ospita il Backend della piattaforma **Exis**, un'applicazione progettata per la gestione sicura di carte di pagamento e movimenti finanziari.
Il sistema espone API RESTful sviluppate in Python con Flask, implementando protocolli di sicurezza avanzati tipici del settore Fintech.

🔗 **Frontend Repository:** [Project Exis FE](https://github.com/mbucci91-dev/project-exis-fe)

## 📋 Caratteristiche Principali

Il progetto adotta un'architettura monolitica a livelli (Layered Architecture) per garantire modularità e sicurezza.

* **Autenticazione Stateless:** Gestione delle sessioni tramite JSON Web Tokens (JWT).
* **Sicurezza Dispositiva (Challenge-Response):** Protocollo di verifica a step per operazioni critiche (es. blocco carta), basato sulla richiesta di indici casuali del PIN segreto.
* **Protezione Dati Sensibili:** Cifratura applicativa simmetrica (AES/Fernet) per la trasmissione protetta di PAN e CVV al frontend.
* **ORM e Database:** Gestione relazionale dei dati (Utenti, Carte, Movimenti) tramite SQLAlchemy.

## 🛠️ Stack Tecnologico

* **Linguaggio:** Python
* **Framework:** Flask
* **Database Toolkit:** SQLAlchemy
* **Security:** `flask_jwt_extended`, `cryptography` (Fernet)

## 📂 Struttura del Progetto

Il codice segue una separazione rigorosa delle responsabilità:

```text
/project-exis-be
│
├── models.py       # Data Layer: Mappatura ORM delle tabelle (User, Card, Movement)
├── routes.py       # Controller Layer: Gestione richieste HTTP e validazione input
├── services.py     # Service Layer: Logica di business, regole di dominio e crittografia
├── seed.py         # Script per il popolamento del database con dati fittizi
├── app.py          # Entry point e configurazione dell'applicazione
├── requirements.txt
└── README.md
```
🚀 Istruzioni di Installazione
1. Prerequisiti
Assicurati di avere Python installato sulla tua macchina.

2. Clona il Repository
Bash

git clone [https://github.com/mbucci91-dev/project-exis-be.git](https://github.com/mbucci91-dev/project-exis-be.git)
cd project-exis-be
3. Configura l'Ambiente Virtuale
È consigliato utilizzare un virtual environment per isolare le dipendenze.

Windows:

Bash

python -m venv venv
venv\Scripts\activate
MacOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate

4. Installa le Dipendenze
Bash

pip install -r requirements.txt
5. Configurazione Variabili d'Ambiente
Crea un file .env nella root del progetto o imposta le variabili di sistema necessarie:

Snippet di codice

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tua_chiave_segreta
JWT_SECRET_KEY=tua_chiave_jwt_super_sicura
💾 Inizializzazione Database
Il progetto include uno script dedicato (seed.py) per inizializzare il database e popolarlo con dati strutturati per i test. Questo script crea utenti, carte multiple e storici di movimenti verosimili.

Bash

python seed.py
Nota: Lo script genererà un database SQLite locale popolato con dati di test (es. Utente: mario, Password: password).

▶️ Avvio del Server
Una volta completata l'installazione e il seeding del database, avvia il server di sviluppo:

Bash

flask run
Il backend sarà accessibile all'indirizzo http://localhost:5000.
