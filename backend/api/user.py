import os
import re
import jwt
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Cookie, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload,joinedload
from sqlalchemy.exc import IntegrityError
from passlib.hash import argon2

# Adjust these imports to point to your actual file location
from db.database import get_db
from db.models import Users, Authentication, Departments, UserTypes

SECRET_KEY = os.getenv("JWT_SECRET", "jakis-ciag-znakow")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN", "60"))
COOKIE_NAME = "access_token" 

# --- UTILS ---
def hash_password(password: str) -> str:
    return argon2.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return argon2.verify(password, password_hash)

def validate_password(password: str) -> str | None:
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

def validate_name(name: str) -> str | None:
    if len(name)<2 or len(name)>15:
        return "Imię musi mieć min. 2 znaki i max. 15 znaków"
    return None

def validate_surname(surname: str) -> str | None:
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

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# --- ROUTER ---
router = APIRouter(prefix="/api/user", tags=["user"])

# --- MODELS (DTOs) ---

# Changed email -> username
class UserCreate(BaseModel):
    username: str 
    name: str
    surname: str
    password: str

class ChangeDetails(BaseModel):
    name: str
    surname: str

# Changed email -> username
class UserRead(BaseModel):
    id: int
    username: str
    name: str
    surname: str

# Changed email -> username
class UserValidate(BaseModel):
    username: str
    password: str


# --- ENDPOINTS ---

@router.post("/register")
async def make_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    
    # Clean inputs
    username_clean = user.username.strip() # Removed .lower() if case sensitivity matters for usernames
    name_clean = user.name.strip()
    surname_clean = user.surname.strip()
    
    # 1. Check if user exists (using user_name column)
    result = await db.execute(select(Users).where(Users.user_name == username_clean))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=409, detail="Nazwa użytkownika jest już zajęta")

    # 2. Validate format
    if error := validate_name(name_clean):
        raise HTTPException(status_code=400, detail=error)
    
    if error := validate_surname(surname_clean):
        raise HTTPException(status_code=400, detail=error)
    
    if error := validate_password(user.password):
        raise HTTPException(status_code=400, detail=error)
        
    # 3. Get Default Foreign Keys (Type & Dept)
    res_type = await db.execute(select(UserTypes).where(UserTypes.type.in_(['user', 'employee'])))
    default_type = res_type.scalars().first()
    if not default_type:
        # Fallback to any type if specific ones aren't found
        res_any_type = await db.execute(select(UserTypes))
        default_type = res_any_type.scalars().first()
        if not default_type:
             raise HTTPException(status_code=500, detail="Błąd konfiguracji: brak ról użytkowników.")

    res_dept = await db.execute(select(Departments))
    default_dept = res_dept.scalars().first()
    if not default_dept:
        raise HTTPException(status_code=500, detail="Błąd konfiguracji: brak działów.")

    try:
        # 4. Create Authentication Record FIRST (to get the PK)
        new_password_hash = hash_password(user.password)
        new_auth = Authentication(password=new_password_hash)
        db.add(new_auth)
        # Flush sends query to DB and populates new_auth.user_id, but doesn't commit transaction yet
        await db.flush() 

        # 5. Create User Record linked to Auth
        new_user = Users(
            auth_id=new_auth.user_id, # Link using the ID generated above
            user_name=username_clean, 
            name=name_clean,
            surname=surname_clean,
            department_id=default_dept.id,
            user_type_id=default_type.id
        )
        db.add(new_user)
        await db.commit()
        
        return {"id": new_user.id, "username": new_user.user_name, "name": new_user.name}

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu użytkownika")


@router.post("/change-details")
async def change_details(
    user: ChangeDetails, 
    db: AsyncSession = Depends(get_db), 
    access_token: str | None = Cookie(default=None, alias=COOKIE_NAME)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Brak tokenu")

    try:
        payload = decode_access_token(access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Niepoprawny token")

    user_id = payload.get("sub")
    
    # Fetch user by ID
    res = await db.execute(select(Users).where(Users.id == int(user_id)))
    db_user = res.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")

    name_clean = (user.name or "").strip()
    surname_clean = (user.surname or "").strip()

    if error := validate_name(name_clean):
        raise HTTPException(status_code=400, detail=error)

    if error := validate_surname(surname_clean):
        raise HTTPException(status_code=400, detail=error)

    db_user.name = name_clean
    db_user.surname = surname_clean

    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu danych")
    
    return {
        "ok": True,
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "surname": db_user.surname,
            "username": db_user.user_name,
        },
    }


@router.get("/all-users", response_model=List[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users))
    users = result.scalars().all()
    return [
        UserRead(
            id=u.id,
            username=u.user_name, # Map user_name to username
            name=u.name,
            surname=u.surname,
        )
        for u in users
    ]


@router.post("/login")
async def login_user(user: UserValidate, db: AsyncSession = Depends(get_db)):
    username_clean = user.username.strip()
     
    # Join necessary tables to get role and password
    query = (
        select(Users)
        .options(
            selectinload(Users.auth),
            selectinload(Users.user_type),
            selectinload(Users.department)
        )
        .where(Users.user_name == username_clean) # Search by user_name
    )
    
    result = await db.execute(query)
    db_user = result.scalars().first()

    # Verify user exists and has auth record
    if not db_user or not db_user.auth:
        raise HTTPException(status_code=401, detail="Nieprawidłowy login lub hasło.")
    
    # Verify password
    if not verify_password(user.password, db_user.auth.password):
         raise HTTPException(status_code=401, detail="Nieprawidłowy login lub hasło.")
     
    # Helper variables
    user_role = db_user.user_type.type if db_user.user_type else "unknown"
    dept_name = db_user.department.type if db_user.department else "unknown"
    dept_id = db_user.department_id

    # Create Token with username
    token_data = {
        "name": db_user.name, 
        "surname": db_user.surname, 
        "username": db_user.user_name, 
        "role": user_role,
        "departmentId": dept_id
    }
    
    token = create_access_token(user_id=db_user.id, user_data=token_data)
    
    # Return full object for Frontend state
    payload = {
        "success": True, 
        "clientId": db_user.id, 
        "name": db_user.name, 
        "surname": db_user.surname, 
        "username": db_user.user_name, 
        "role": user_role,
        "departmentId": dept_id,
        "departmentName": dept_name
    }
    
    response = JSONResponse(content=payload, status_code=200)
    response.set_cookie(
        key=COOKIE_NAME, 
        value=token, 
        httponly=True, 
        samesite="lax", 
        secure=False, 
        max_age=60*60, 
        path="/"
    )
    
    return response

# Logout and check_login remain mostly the same, just updated variable names in payload
@router.post("/logout")
async def logout_user():
    response = JSONResponse(content={"success": True})
    response.delete_cookie(key=COOKIE_NAME, path="/")
    return response


@router.get("/is_login")
async def is_user_login(access_token: str | None = Cookie(default=None, alias=COOKIE_NAME)):
    if not access_token:
        return {"islogin": False, "user": None}
    
    try:
        payload = decode_access_token(access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    except Exception:
        raise HTTPException(status_code=401, detail="Błąd tokenu")
    
    return {
        "islogin": True,   
        "user": {
            "id": payload.get("sub"), 
            "name": payload.get("name"),  
            "surname": payload.get("surname"), 
            "username": payload.get("username"),
            "role": payload.get("role"),
            "departmentId": payload.get("departmentId")
        }
    }

async def get_current_user(
    access_token: str | None = Cookie(default=None, alias=COOKIE_NAME),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if not access_token:
        raise credentials_exception

    try:
        # 1. Decode the token using your settings
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extract User ID ('sub' from your create_access_token function)
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.InvalidTokenError:
        raise credentials_exception

    # 3. Fetch User from DB
    # We load 'user_type' because the redirection logic needs to check if they are admin
    query = (
        select(Users)
        .where(Users.id == int(user_id_str))
        .options(joinedload(Users.user_type)) 
    )
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise credentials_exception
        
    return user