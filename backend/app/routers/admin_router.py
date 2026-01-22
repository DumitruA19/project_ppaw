from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import require_admin,get_current_admin
from app.models import schema as s
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Control Panel"])

@router.get("/users", response_model=list[s.UserOut], dependencies=[Depends(require_admin)])
def get_all_users(db: Session = Depends(get_db)):
    """Afișează toți utilizatorii din sistem."""
    return AdminService(db).list_users()

# app/routers/admin_router.py

@router.put("/users/{user_id}", dependencies=[Depends(require_admin)])
def modify_user(
    user_id: str, 
    data: dict, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin) # Obținem obiectul admin pentru logare
):
    """Endpoint pentru actualizarea datelor unui utilizator."""
    try:
        # Trimitem ID-ul admin-ului pentru a fi înregistrat în loguri
        return AdminService(db).update_user(user_id, data, admin_id=current_admin.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/plans", dependencies=[Depends(require_admin)])
def add_new_plan(data: dict, db: Session = Depends(get_db)):
    """Creează un nou plan tarifar."""
    try:
        return AdminService(db).create_billing_plan(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/plans/{plan_id}", dependencies=[Depends(require_admin)])
def stop_plan(plan_id: int, db: Session = Depends(get_db)):
    """Dezactivează un plan fără a-l șterge fizic."""
    try:
        return AdminService(db).deactivate_billing_plan(plan_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Folosim require_admin pentru rutele care nu au nevoie de obiectul 'user'
@router.get("/users", response_model=list[s.UserOut], dependencies=[Depends(require_admin)])
def get_all_users(db: Session = Depends(get_db)):
    return AdminService(db).list_users()

# app/routers/admin_router.py

@router.put("/users/{user_id}", dependencies=[Depends(require_admin)])
def modify_user(
    user_id: str, 
    data: dict, 
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin) # Obținem administratorul curent
):
    """Actualizează datele unui utilizator și înregistrează acțiunea."""
    try:
        # Trimitem admin.id pentru logul de succes: ADMIN_USER_UPDATE_SUCCESS
        return AdminService(db).update_user(user_id, data, admin_id=admin.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/logs")
def get_admin_logs(
    db: Session = Depends(get_db), 
    current_admin = Depends(get_current_admin) 
):
    """Endpoint pentru vizualizarea logurilor de audit."""
    return AdminService(db).get_logs()

@router.post("/users", dependencies=[Depends(require_admin)])
def admin_create_user(data: dict, db: Session = Depends(get_db)):
    """Creează un utilizator direct de către administrator."""
    try:
        return AdminService(db).create_user(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    # app/routers/admin_router.py

# ... restul rutelor existente ...

@router.delete("/users/{user_id}", dependencies=[Depends(require_admin)])
def remove_user(user_id: str, db: Session = Depends(get_db)):
    """Elimină definitiv un utilizator din sistem."""
    try:
        # Apelează serviciul pe care l-ai verificat anterior
        return AdminService(db).delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))