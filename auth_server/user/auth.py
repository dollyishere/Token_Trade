import os
import environ
from pathlib import Path
import jwt
import datetime
import pytz

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

SECRET_KEY = env("AUTH_SERVER_SECRET_KEY")
ALGORITHM = "HS256"
KST = pytz.timezone("Asia/Seoul")


def create_access_token(username, is_manager):
    """access token 발급"""
    now = datetime.datetime.now(KST)
    exp = now + datetime.timedelta(minutes=15)

    role = "none"

    if is_manager:
        role = "manager"

    payload = {"username": username, "role": role, "exp": exp, "iat": now}
    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return access_token


def create_refresh_token(username, is_manager):
    """refresh token 발급"""
    now = datetime.datetime.now(KST)
    exp = now + datetime.timedelta(days=7)

    role = "none"

    if is_manager:
        role = "manager"

    payload = {"username": username, "role": role, "exp": exp, "iat": now}
    refresh_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return refresh_token
