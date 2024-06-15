import datetime
import secrets

from fastapi import FastAPI, HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from typing import Optional, List

from util.MySQL import MySQL
from util.logWriter import logWriter
from query.mysql_query import *

# def load_config():
#     # 설정 파일에서 값을 읽어와서 전역 변수에 저장
#     with open("config.yaml", "r") as f:
#         global config
#         config = yaml.safe_load(f)
    
#     return config


class AuthHandler():
    def __init__(self):
        
        self.conf = None
    
    def mysql_connect(self):
        try:
            mysql = MySQL()
            mysql.connect(
                user="root",
                password="",
                host="root",
                port="",
                database=""
            )
            logWriter.log.info("MYSQL connect success")
            return mysql
        except Exception as e:
            logWriter.log.error("MYSQL connect fail")
            logWriter.log.error(e)

    def __init__(self):
        # self.conf = load_config()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def mysql_connect(self):
        try:
            mysql = MySQL()
            mysql.connect(
                user="root",
                password="",
                host="root",
                port="",
                database=""
            )
            logWriter.log.info("MYSQL connect success")
            return mysql
        except Exception as e:
            logWriter.log.error("MYSQL connect fail")
            logWriter.log.error(e)

    def get_user(self, mysql, username: str):
        mysql.clearBind()
        mysql.addBind('USERNAME', username)
        dt = mysql.select(selectUser)
        user_dict = dt[0]

        return user_dict
    
    def get_key(self, mysql):
        mysql.clearBind()
        dt = mysql.select(selectSecretKey)

        if len(dt) == 0:
            sec_key = self.generate_secret_key()
            ref_key = self.generate_secret_key()
            
            mysql.clearBind()
            mysql.addBind('SEC_KEY', sec_key)
            mysql.addBind('REF_KEY', ref_key)
            mysql.execute(insertKey)
        
        else:
            sec_key, ref_key = dt[0]['sec_key'], dt[0]['ref_key']

        return sec_key, ref_key
    
    def generate_secret_key(self, length=32):
        return secrets.token_hex(length)


    def create_access_token(self, data: dict, secret_key, algorithm, expires_delta: Optional[datetime.timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now() + expires_delta
        else:
            expire = datetime.datetime.now() + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict, secret_key, algorithm, expires_delta: Optional[datetime.timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now() + expires_delta
        else:
            expire = datetime.datetime.now() + datetime.timedelta(minutes=60*24*7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    def get_user(self, mysql, username: str):
        mysql.clearBind()
        mysql.addBind('USERNAME', username)
        dt = mysql.select(selectUser)
        user_dict = dt[0]

        return user_dict

    def authenticate_user(self, mysql, username: str):
        user = self.get_user(mysql, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect API Key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def verify_token(self, data, secret_key, algorithm='HS256'):
        try:
            token = data.split(" ")[1]
            msg = jwt.decode(token, secret_key, algorithms=[algorithm])
            # print(msg)
            return True, msg
        
        # token 없는 경우
        except AttributeError:
            return False, {'error': 'token required'}
        
        except IndexError:
            return False, {'error': 'token required'}
        
        # token 만료
        except jwt.ExpiredSignatureError:
            return False, {'error': 'expired_token'}
        
        # token 유효하지 않음
        except (jwt.JWTClaimsError, jwt.JWTError) as e:
            return False, {'error': 'invalid_token', 'detail': str(e)}
