from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import create_access_token
from db.repository.login import authenticate_user
from db.session import get_db
from schemas.schemas import Token


router = APIRouter()


@router.post('/token', response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Get access token for request user."""
    user = authenticate_user(form_data.username, form_data.password, db)
    return {
        'access_token': create_access_token(
            data={'username': user.username, 'password': user.password}),
        'token_type': 'Bearer'
    }
