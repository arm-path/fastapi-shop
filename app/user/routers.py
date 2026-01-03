from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.settings.database import SessionDepends
from app.user.schemas import RegistrationSchema, Token, CurrentUserSchema
from app.user.services import AuthUserService, CurrentUserDepends

router = APIRouter(prefix='/users', tags=['User'])


@router.post('/registration/', status_code=status.HTTP_204_NO_CONTENT)
async def registration(data: RegistrationSchema, session: SessionDepends):
    return await AuthUserService.registration(session, data)


@router.post('/authentication/', response_model=Token)
async def authentication(session: SessionDepends, data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await AuthUserService.authentication(session, data)


@router.get('/me/', response_model=CurrentUserSchema)
async def me(user: CurrentUserDepends):
    return user
