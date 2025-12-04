from typing import Dict
import jwt 
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext 
from datetime import datetime, timedelta, UTC
import dateparser
import time
from settings.config import load_env_config
from database.model import create_auth_token, get_latest_user_auth_token, get_single_user_by_id, update_auth_token, update_user_auth_token
from database.db import session, has_uncommitted_changes, get_laravel_datetime
from sqlalchemy.orm import Session
import hashlib
import json
from settings.constants import USER_TYPES

config = load_env_config()

def get_next_few_minutes(minutes: int=0):
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=minutes)
    return future_time.strftime("%Y-%m-%d %H:%M:%S")

def check_if_time_as_pass_now(time_str: str = None):
    date_parsed = dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
    time_tz = time.mktime(date_parsed.timetuple())
    time_tz = int(time_tz)
    current_tz = int(time.time())
    if current_tz >= time_tz:
        return True
    else:
        return False

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = config['secret_key']
    db = session

    def get_password_hash(self, password: str = None):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str=None, hashed_password: str=None):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user: Dict={}, device_token: str = None):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=365),
            'iat': datetime.utcnow(),
            'sub': json.dumps(user)
        }
        expired_at = (datetime.utcnow() + timedelta(days=365)).strftime("%Y/%m/%d %H:%M:%S")
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        user_id = user['id']
        update_user_auth_token(db=self.db, user_id=user_id, values={'status': 0}, commit=True)
        create_auth_token(db=self.db, user_id=user_id, token=token, device_token=device_token, status=1, expired_at=expired_at, commit=True)
        return token

    def decode_token(self, token: str = None):
        try:
            if isinstance(token, bytes):
                token = token.decode('utf-8')
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            sub_data = json.loads(payload['sub'])
            user_id = sub_data['id']
            user = get_single_user_by_id(db=self.db, id=user_id)
            if user is None:
                raise HTTPException(status_code=401, detail='User does not exist')
            else:
                auth_token = get_latest_user_auth_token(db=self.db, user_id=user_id)
                if auth_token is None:
                    raise HTTPException(status_code=401, detail='Empty Auth Token')
                else:
                    if auth_token.token != token:
                        raise HTTPException(status_code=401, detail='Invalid Auth Token')
                    else:
                        if auth_token.status == 0:
                            raise HTTPException(status_code=401, detail='Token Expired')
                        else:
                            if user.user_type != USER_TYPES['bank']['num']:
                                raise HTTPException(status_code=401, detail='Invalid User Type')
                            deleted_at = user.deleted_at
                            if deleted_at is not None:
                                raise HTTPException(status_code=401, detail='User is deleted')
                            else:
                                update_auth_token(db=self.db, id=auth_token.id, values={'last_ping_at': get_laravel_datetime()}, commit=True)
                                return sub_data
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
