import uuid
import logging
from passlib.context import CryptContext
from datetime import datetime, timedelta, time, timezone
import jwt 
from src.config import Config
import logging

passwd_context = CryptContext(
    schemes=['bcrypt']
)

# time in seconds
ACCESS_TOKEN_EXPIRY = 3600

def generate_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash 

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    now = datetime.now(timezone.utc)
    expire_delta = expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    expire_time = now + expire_delta

    logging.info(f"Token created at: {now}")
    logging.info(f"Token expires at: {expire_time}")

    payload = {
        'user': user_data,
        'exp': int(expire_time.timestamp()),
        'iat': int(now.timestamp()),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }


    # payload = {}

    # payload['user'] = user_data
    # payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    # payload['jti'] = str(uuid.uuid4())
    # payload['refresh'] = refresh

    print(payload)

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


# def decode_token(token: str) -> dict:
#     try:
#         token_data = jwt.decode(
#             jwt=token,
#             key=Config.JWT_SECRET,
#             algorithms=[Config.JWT_ALGORITHM],
#         )

#         return token_data if token_data['exp'] >= time.time() else None
#     except jwt.PyJWTError as e:
#         logging.exception(e)
#         return None 
    
def decode_token(token: str) -> dict | None:
    """Decode and validate JWT token with detailed logging"""
    try:
        # First decode without verification to check the payload
        unverified_payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
            options={'verify_exp': False}  # Temporarily disable exp verification
        )
        
        # Log the token details for debugging
        now = datetime.now(timezone.utc)
        exp_time = datetime.fromtimestamp(unverified_payload['exp'], tz=timezone.utc)
        iat_time = datetime.fromtimestamp(unverified_payload['iat'], tz=timezone.utc)
        
        logging.info(f"Current time (UTC): {now}")
        logging.info(f"Token exp time (UTC): {exp_time}")
        logging.info(f"Token iat time (UTC): {iat_time}")
        logging.info(f"Time until expiration: {exp_time - now}")
        
        # Now do the actual verification
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        
        return token_data
        
    except jwt.ExpiredSignatureError as e:
        logging.error(f"Token expired: {str(e)}")
        return None
    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error decoding token: {str(e)}")
        return None