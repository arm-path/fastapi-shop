from fastapi import APIRouter, status

from app.settings.database import SessionDepends
from app.user.schemas import RegistrationSchema, UserBaseSchema, AuthSchema
from app.user.services import AuthUserService

router = APIRouter(prefix='/users', tags=['User'])


@router.post('/registration/', status_code=status.HTTP_204_NO_CONTENT)
async def registration(data: RegistrationSchema, session: SessionDepends):
    return await AuthUserService.registration(session, data)

@router.post('/authentication/', response_model=UserBaseSchema)
async def authentication(data: AuthSchema, session: SessionDepends):
    return await AuthUserService.authentication(session, data)