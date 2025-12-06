from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel, EmailStr
from db.database import get_db
from db.models import Clients
from db.models import UserAuth
import re

from passlib.hash import argon2

import jwt
import os
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("JWT_SECRET", "jakis-ciag-znakow")   ## w wersji produkcyjnej do zmiany na os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN", "60"))
COOKIE_NAME = "access_token" 


def hash_password(password: str) -> str:
    return argon2.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return argon2.verify(password, password_hash)

def validate_password(password: str) -> str:
    if len(password) < 8:
        return "Hasło musi mieć min. 8 znaków"
    if not re.search(r"[A-Z]", password):
        return "Hasło musi posiadać przynajmniej jedną wielką literę"
    if not re.search(r"[a-z]", password):
        return "Hasło musi posiadać przynajmniej jedną małą literę"
    if not re.search(r"[0-9]", password):
        return "Hasło musi posiadać przynajmniej jedną cyfrę"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Hasło musi posiadać przynajmniej jeden znak specjalny"
    return None

def validate_name(name: str) -> str:
    if len(name)<2 or len(name)>15:
        return "Imię musi mieć min. 2 znaki i max. 15 znaków"
    return None

def validate_surname(surname: str) -> str:
    if len(surname)<2 or len(surname)>15:
        return "Nazwisko musi mieć min. 2 znaki i max. 15 znaków"
    return None

def create_access_token(user_id: int, user_data: dict | None = None, expires_minutes: int | None = None) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MIN)
    
    payload ={
        "sub": str(user_id), 
        "exp": int(exp.timestamp()),
        **(user_data or {})
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) ->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



router = APIRouter(prefix="/api/user", tags=["user"])

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str

@router.post("/register")
async def make_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    
    user.email = user.email.lower().strip()
    user.name = user.name.strip()
    user.surname = user.surname.strip()
    
    result = await db.execute(select(Clients).where(Clients.mail == user.email))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=409, detail="Istnieje konto zarejestrowane na ten Email")

    name_error = validate_name(user.name)
    if name_error:
        raise HTTPException(status_code=400, detail=name_error)
    
    surname_error = validate_surname(user.surname)
    if surname_error:
        raise HTTPException(status_code=400, detail=surname_error)
    
    password_error = validate_password(user.password)
    if password_error:
        raise HTTPException(status_code=400, detail=password_error)
        
    new_client = Clients(
         mail = user.email,
         name = user.name,
         surname = user.surname
    )
    db.add(new_client)
    await db.flush()

    new_password_hash = hash_password(user.password)
    
    new_user_auth = UserAuth (client_id = new_client.id, password_hash = new_password_hash,  role="user", is_active=True)
    db.add(new_user_auth)
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu użytkownika")
    
    return {"id": new_client.id, "email": new_client.mail, "name": new_client.name}


class ChangeDetails(BaseModel):
    name: str
    surname: str


@router.post("/change-details")
async def change_details( user: ChangeDetails, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None),):
    if not access_token:
        raise HTTPException(status_code=401, detail="Brak tokenu")

    try:
        payload = decode_access_token(access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    except Exception:
        raise HTTPException(status_code=401, detail="Niepoprawny token")

    user_id = payload.get("sub")
    user_id_raw = payload.get("sub")
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Niepoprawny token")
        
    res = await db.execute(select(Clients).where(Clients.id == user_id))
    client = res.scalars().first()
    if not client:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")

    name = (user.name or "").strip()
    surname = (user.surname or "").strip()

  
    name_error = validate_name(name)
    if name_error:
        raise HTTPException(status_code=400, detail=name_error)

    surname_error = validate_surname(surname)
    if surname_error:
        raise HTTPException(status_code=400, detail=surname_error)


    client.name = name
    client.surname = surname          

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu użytkownika")
    
    await db.refresh(client)

    return {
        "ok": True,
        "user": {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "email": client.mail,
        },
    }



class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str

@router.get("/all-users", response_model=List[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Clients))
    clients = result.scalars().all()
    return [
        UserRead(
            id=o.id,
            email=o.mail,
            name=o.name,
            surname=o.surname,
        )
        for o in clients
    ]
    
class UserValidate(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login_user(user: UserValidate, db: AsyncSession = Depends(get_db)):
    
    user.email = user.email.lower().strip()
     
    cli = await db.execute(select(Clients).where(Clients.mail == user.email))
    client = cli.scalars().first()
    if not client:
        raise HTTPException(status_code=401, detail="Nieprawidłowy email lub hasło.")
    
    aut =  await db.execute(select(UserAuth).where(UserAuth.client_id == client.id))
    client_aut = aut.scalars().first()
    
    if not client_aut or not verify_password(user.password, client_aut.password_hash):
         raise HTTPException(status_code=401, detail="Nieprawidłowy email lub hasło.")
     

    token = create_access_token(user_id=client.id, user_data={"name": client.name, "surname": client.surname, "email": client.mail, "role": client_aut.role})
    
    payload = {"success": True, "clientId": client.id, "name": client.name, "surname": client.surname, "email": client.mail, "role": client_aut.role}
    
    response = JSONResponse(content=payload, status_code=200)
    response.set_cookie(key=COOKIE_NAME, value=token, httponly=True, samesite="lax", secure=False, max_age=60*60, path="/",)  ## w prod secure=True, jak będzie działal https
    
    return response

@router.post("/logout")
async def logout_user():
    response = JSONResponse(content={"success": True})
    response.delete_cookie(key=COOKIE_NAME, path="/")
    return response


@router.get("/is_login")
async def is_user_login(access_token: str = Cookie(None)):
    if not access_token:
        return {"islogin": False, "user": None}
    
    try:
        payload = decode_access_token(access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    except Exception:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    
    return {"islogin": True,   "user": {"id": payload.get("sub"), "name": payload.get("name"),  "surname": payload.get("surname"), "email": payload.get("email")}}