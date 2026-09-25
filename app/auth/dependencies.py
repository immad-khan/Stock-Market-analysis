# app/auth/dependencies.py

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Reads user_id from the session cookie (set at login),
    fetches the User from DB. Raises 401 if not logged in.
    """
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user