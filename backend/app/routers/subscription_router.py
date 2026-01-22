from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import get_current_user
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["Billing Logic"])

@router.post("/create")
def create_sub(plan: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Asigură-te că AuthService sau SubscriptionService primește corect user.id
    return SubscriptionService(db).create_subscription(current_user.id, plan)

@router.get("/status")
def check_limit(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Verifică dreptul de utilizare."""
    allowed = SubscriptionService(db).can_use_feature(user.id)
    return {"allowed": allowed}



@router.get("/check")
def check_limit(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Verifică dacă utilizatorul mai are mesaje disponibile."""
    # Această logică va fi apelată de frontend înainte de trimiterea mesajului
    from app.services.subscription_service import SubscriptionService
    try:
        # Folosim o metodă care verifică dacă limita a fost atinsă
        SubscriptionService(db).check_usage_limit(current_user.id)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/consume")
def consume_message(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Consumă un credit de mesaj."""
    return SubscriptionService(db).consume_attempt(current_user.id)


# ... restul importurilor tale ...

@router.post("/checkout")
def checkout_simulation(
    data: dict, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """Simulează procesarea plății și o salvează în tabela 'payments'."""
    from app.models import sql_models as m
    
    # Creăm o înregistrare în tabela de plăți pentru a simula tranzacția
    new_payment = m.Payment(
        user_id=current_user.id,
        amount=data.get("amount", 0) / 100, # Convertim din cenți în unități întregi (ex: 499 -> 4.99)
        currency=data.get("currency", "EUR"),
        status="succeeded"
    )
    db.add(new_payment)
    db.commit()
    
    return {"message": "Plată procesată cu succes", "payment_id": new_payment.id}