from app import app, db
from models import User, Card, Movement
from keys import *
from datetime import datetime

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
            cvv="123",
            circuit=C_VISA
        )
        
        mastercard = Card(
            pan="5100123456789010", 
            holder="MARIO ROSSI", 
            exp_date="08/25", 
            user_id=mario.id,
            status=S_CARD_BLOCKED,
            cvv="123",
            circuit=C_MASTERCARD 
        )
        
        db.session.add(visa)
        db.session.add(mastercard)
        db.session.commit()

        mov1 = Movement(amount=-50.00, description="Spesa Carrefour", card_id=visa.id, date=datetime(2025, 12, 1, 14, 30))
        db.session.add(mov1)

        mov3 = Movement(amount=-150.00, description="Amazon", card_id=visa.id, date=datetime(2025, 12, 4, 17, 32))
        db.session.add(mov3)

        mov4 = Movement(amount=-33.36, description="Cena", card_id=visa.id, date=datetime(2025, 12, 5, 22, 32))
        db.session.add(mov4)
        
        mov2 = Movement(amount=-800.00, description="Acquisto Laptop", card_id=mastercard.id, date=datetime(2025, 12, 3, 17, 00))
        db.session.add(mov2)

        mov5 = Movement(amount=-88.00, description="Sushi", card_id=mastercard.id, date=datetime(2025, 11, 29, 21, 00))
        db.session.add(mov5)

        mov6 = Movement(amount=-350.00, description="Assicurazione", card_id=mastercard.id, date=datetime(2025, 11, 27, 12, 1))
        db.session.add(mov6)

        mov7 = Movement(amount=-12.50, description="Bar", card_id=mastercard.id, date=datetime(2025, 12, 1, 8, 00))
        db.session.add(mov7)

        luigi = User(username="luigi", password="test123", status=S_USER_BLOCKED, secret_pin="12345")
        db.session.add(luigi)

        db.session.commit()
        print("Database popolato con nuovi stati!")

if __name__ == "__main__":
    seed_data()