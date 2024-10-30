from typing import List, Any
from src.utils import decode_token
from sqlmodel import select, delete
from fastapi.security import HTTPBearer 
from datetime import datetime, timedelta
from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from src.db.database import get_session
from src.models.token_blocklist import TokenBlocklist  
from sqlmodel.ext.asyncio.session import AsyncSession 
from fastapi.security.http import HTTPAuthorizationCredentials
from src.services.cust_auth import CustAuthService

from src.models.cust_auth import CustAuth
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
    AccountNotVerified,
)

cust_auth_service = CustAuthService()

JTI_EXPIRY = 3600
class TokenBlocklistService:
    @staticmethod
    async def add_jti_to_blocklist(jti: str, session: AsyncSession) -> None:
        expiry_at = datetime.now() + timedelta(seconds=JTI_EXPIRY)
        block_entry = TokenBlocklist(jti=jti, expiry_at=expiry_at)
        session.add(block_entry)
        await session.commit()

    @staticmethod
    async def token_in_blocklist(jti: str, session: AsyncSession) -> bool:
        statement = select(TokenBlocklist).where(TokenBlocklist.jti == jti, TokenBlocklist.expiry_at > datetime.now())
        result = await session.exec(statement)
        return result is not None
    
    @staticmethod
    async def clean_expired_tokens(session: AsyncSession) -> None:
        statement = delete(TokenBlocklist).where(
            TokenBlocklist.expiry_at <= datetime.now()
        )
        await session.execute(statement)
        await session.commit()

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()
        # , session: AsyncSession = Depends(get_session)
        # if await TokenBlocklistService.token_in_blocklist(token_data['jti'], session):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail={
        #             "error": "This token is invalid or has been revoked.",
        #             "resolution": "Please get a new token."
        #         }
        #     )

        self.verify_token_data(token_data)
        # await TokenBlocklistService.clean_expired_tokens(session)
        return token_data
    
    def token_valid(self, token: str) -> bool:
        '''Checks if access token is valid and returns boolean.'''
        token_data = decode_token(token)

        return token_data is not None
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes.")
    

    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()
        

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()
        

async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
    ):

    user_email = token_details['user']['email'] 
    user = await cust_auth_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: CustAuth = Depends(get_current_user)) -> Any:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return True 
        
        raise InsufficientPermission()