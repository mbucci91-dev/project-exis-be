from app import app, db
from models import User, Card, Movement
from keys import *

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        mario = User(username="mario", password="test123", status=S_USER_ACTIVE, secret_pin="12345")
        db.session.add(mario)
        db.session.commit()

        visa = Card(
            pan="4000123456789010", 
            holder="MARIO ROSSI", 
            exp_date="12/26", 
            user_id=mario.id,
            status=S_CARD_ACTIVE,
            cvv="123"
        )
        
        mastercard = Card(
            pan="5100123456789010", 
            holder="MARIO ROSSI", 
            exp_date="08/25", 
            user_id=mario.id,
            status=S_CARD_BLOCKED,
            cvv="123" 
        )
        
        db.session.add(visa)
        db.session.add(mastercard)
        db.session.commit()

        mov1 = Movement(amount=-50.00, description="Spesa", card_id=visa.id)
        db.session.add(mov1)
        
        mov2 = Movement(amount=-800.00, description="Acquisto Laptop", card_id=mastercard.id)
        db.session.add(mov2)

        luigi = User(username="luigi", password="test123", status=S_USER_BLOCKED, secret_pin="12345")
        db.session.add(luigi)

        db.session.commit()
        print("Database popolato con nuovi stati!")

if __name__ == "__main__":
    seed_data()