from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete  
from typing import List, Optional
from sqlalchemy.exc import IntegrityError


from db.database import get_db
from fastapi import APIRouter, HTTPException
from db.models import Object
from db.models import Global
from db.models import Reservations

from pydantic import BaseModel, Field
from pathlib import Path
import json

import jwt
import os
from datetime import time
from decimal import Decimal
from datetime import date


SECRET_KEY = os.getenv("JWT_SECRET", "jakis-ciag-znakow")   ## w wersji produkcyjnej do zmiany na os.environ["JWT_SECRET"]
ALGORITHM = "HS256"


def decode_access_token(token: str) ->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def require_token(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Brak tokenu uwierzytelniającego")

    try:
        payload = decode_access_token(access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    except Exception:
        raise HTTPException(status_code=401, detail="Błąd weryfikacji tokenu")

    return payload

def to_minutes(x) -> int:
    return int(x * 60)


def validate_name(name: str)  -> Optional[str]:
    if len(name)<3 or len(name)>25:
        return "Nazwa obiektu musi mieć min. 3 znaki i max. 25 znaków"
    return None

def validate_desc(desc: str)  -> Optional[str]:
    if len(desc)<3 or len(desc)>40:
        return "Opis obiektu musi mieć min. 3 znaki i max. 40 znaków"
    return None

def validate_discypline(name: str) -> Optional[str]:
    name = name.strip()
    if len(name)<2 or len(name)>15:
        return "Dyscyplina musi mieć min. 2 znaki i max. 15 znaków"
    return None

def validate_opening_hour_and_closing_hour(openingHour: time, closingHour: time, globOpeningHour: time, globClosingHour: time)-> Optional[str]:
    if globOpeningHour> openingHour:
        return "Godziny otwarcia obiektu nie możw być wcześniejsza niż godzina otwarcia klubu"
    if globClosingHour< closingHour:
        return "Godziny zamknięcia obiektu nie możw być póżniejsza niż godzina zakmnięcia klubu"
    if  not openingHour or not closingHour:
        return "Godziny otwarcia i zamknięcia są wymagane"
    if closingHour < openingHour:
        return "Godzina zamknięcia nie może być wcześniejsza niż godzina otwarcia"
    return None

def validate_timeBlock(timeBlock: float, globalTimeBlock: float) -> Optional[str]:
    tb = to_minutes(timeBlock)
    gtb = to_minutes(globalTimeBlock)

    if tb < gtb:
        return "Krok obiektu nie może być mniejszy niż krok klubu"
    if tb < 15:
        return "Krok musi być co najmniej 15 minut"
    if tb > 120:
        return "Krok nie może przekraczać 120 minut"
    if tb % gtb != 0:
        return "Krok obiektu musi być wielokrotnością kroku klubu"
    return None

def validate_minimalTimeBlock(timeBlock: float, minimalTimeBlock: float, globalMinimalTimeBlock: float) -> Optional[str]:
    tb  = to_minutes(timeBlock)
    minb = to_minutes(minimalTimeBlock)
    gmin = to_minutes(globalMinimalTimeBlock)

    if minb < gmin:
        return "Minimalny czas rezerwacji nie może być krótszy niż minimalny czas rezerwacji klubu"
    if minb < tb:
        return "Minimalny czas nie może być krótszy niż krok"
    if minb % tb != 0:
        return "Minimalny czas musi być wielokrotnością kroku"
    return None

def validate_maximalTimeBlock(timeBlock: float, minimalTimeBlock: float, maximalTimeBlock: float, globalMaximalTimeBlock: float) -> Optional[str]:
    tb  = to_minutes(timeBlock)
    minb = to_minutes(minimalTimeBlock)
    maxb = to_minutes(maximalTimeBlock)
    gmax = to_minutes(globalMaximalTimeBlock)

    if maxb > gmax:
        return "Maksymalny czas rezerwacji nei może być więkzy niż maksymalny czas rezerwacji klubu"
    if minb > maxb:
        return "Maksymalny czas musi być ≥ minimalnego"
    if maxb % tb != 0:
        return "Maksymalny czas musi być wielokrotnością kroku"
    return None



router = APIRouter(prefix="/api/objects", tags=["objects"])

@router.get("/", response_model=List[dict])
async def get_objects(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Object))
    objects = result.scalars().all()
    return [
        {
            "id": o.id,
            "name": o.name,
            "discipline": o.discipline,
            "description": o.description,
            "opening_hour": o.opening_hour.strftime("%H:%M") if o.opening_hour else None,
            "closing_hour": o.closing_hour.strftime("%H:%M") if o.closing_hour else None,
            "time_block": float(o.time_block),
            "minimal_time_block": float(o.minimal_time_block),
            "maximal_time_block": float(o.maximal_time_block),
        }
        for o in objects
    ]


@router.get("/id", response_model=List[dict])
async def get_objects_id(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Object))
    objects = result.scalars().all()
    return [
        {
            "id": o.id,
            "name": o.name,
            "discipline": o.discipline,
            "description": o.description,
        }
        for o in objects
    ]

@router.get("/for_object", response_model=List[dict])
async def for_object(id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Object).where(Object.id == id))
    objects = result.scalars().all()
    return [
        {
            "id": o.id,
            "name": o.name,
            "discipline": o.discipline,
            "description": o.description,
            "opening_hour": o.opening_hour.strftime("%H:%M") if o.opening_hour else None,
            "closing_hour": o.closing_hour.strftime("%H:%M") if o.closing_hour else None,
            "time_block": float(o.time_block),
            "minimal_time_block": float(o.minimal_time_block),
            "maximal_time_block": float(o.maximal_time_block),
        }
        for o in objects
    ]

class NextId(BaseModel):
    id: int

@router.get("/next_free_id", response_model=NextId)
async def next_free_id(db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):

    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    result = await db.execute(select(Object))
    objects = result.scalars().all()
    if not objects:
        return NextId(id=1)

    max_id=0

    for i in objects:
        if i.id>max_id:
            max_id = i.id

    return NextId(id=max_id + 1)

class NewObject(BaseModel):
    id: int
    name: str
    desc: str
    disc: str

    openingHour: time
    closingHour: time
    
    timeBlock: float
    minimalTimeBlock: float
    maximalTimeBlock: float


@router.post("/add_new_object")
async def add_new_object(new_data: NewObject, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):

    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")

    glob_res = await db.execute(select(Global))
    glob = glob_res.scalars().first()
    if not glob:
        raise HTTPException(status_code=404, detail="Global settings not found") 

    error = validate_name(new_data.name)
    if error:
        raise HTTPException(status_code=400, detail=error)

    error = validate_desc(new_data.desc)
    if error:
        raise HTTPException(status_code=400, detail=error)

    error = validate_discypline(new_data.disc)
    if error:
        raise HTTPException(status_code=400, detail=error)

    error = validate_opening_hour_and_closing_hour(new_data.openingHour, new_data.closingHour, glob.opening_hour, glob.closing_hour)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_timeBlock(new_data.timeBlock, glob.time_block)
    if error:
        raise HTTPException(status_code=400, detail=error)
       
    error = validate_minimalTimeBlock(new_data.timeBlock, new_data.minimalTimeBlock, glob.minimal_time_block)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_maximalTimeBlock(new_data.timeBlock, new_data.minimalTimeBlock, new_data.maximalTimeBlock, glob.maximal_time_block)
    if error:
        raise HTTPException(status_code=400, detail=error)

    new_obj = Object(
        id=new_data.id,
       name = new_data.name,
       description = new_data.desc,
       discipline= new_data.disc,
       opening_hour = new_data.openingHour,
       closing_hour = new_data.closingHour,
       time_block = new_data.timeBlock,
       minimal_time_block = new_data.minimalTimeBlock,
       maximal_time_block = new_data.maximalTimeBlock,
    )

    db.add(new_obj)
    await db.flush()
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu nowego obiektu")
    
    return {"ok": True}

class EditedObject(BaseModel):
    id: int
    name: str
    desc: str
    disc: str

    openingHour: time
    closingHour: time
    
    timeBlock: float
    minimalTimeBlock: float
    maximalTimeBlock: float


@router.post("/edit_object")
async def edit_object(new_data: EditedObject, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):

    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    result = await db.execute(select(Object).where(Object.id == new_data.id))
    object_to_edit = result.scalars().first()

    if not object_to_edit:
        raise HTTPException(status_code=404, detail="Nie znaleziono obiektu o podanym id")

    glob_res = await db.execute(select(Global))
    glob = glob_res.scalars().first()
    if not glob:
        raise HTTPException(status_code=404, detail="Global settings not found") 

    
    error = validate_name(new_data.name)
    if error:
        raise HTTPException(status_code=400, detail=error)

    error = validate_desc(new_data.desc)
    if error:
        raise HTTPException(status_code=400, detail=error)

    error = validate_discypline(new_data.disc)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_opening_hour_and_closing_hour(new_data.openingHour, new_data.closingHour, glob.opening_hour, glob.closing_hour)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_timeBlock(new_data.timeBlock, glob.time_block)
    if error:
        raise HTTPException(status_code=400, detail=error)
       
    error = validate_minimalTimeBlock(new_data.timeBlock, new_data.minimalTimeBlock, glob.minimal_time_block)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_maximalTimeBlock(new_data.timeBlock, new_data.minimalTimeBlock, new_data.maximalTimeBlock, glob.maximal_time_block)
    if error:
        raise HTTPException(status_code=400, detail=error)

    object_to_edit.name = new_data.name
    object_to_edit.description = new_data.desc
    object_to_edit.discipline= new_data.disc
    object_to_edit.opening_hour = new_data.openingHour
    object_to_edit.closing_hour = new_data.closingHour
    object_to_edit.time_block = new_data.timeBlock
    object_to_edit.minimal_time_block = new_data.minimalTimeBlock
    object_to_edit.maximal_time_block = new_data.maximalTimeBlock
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany danych obiektu")
    
    return {"ok": True}

class DeleteObject(BaseModel):
    id: int


@router.delete("/delate/{object_id}")
async def delete_object(object_id: int, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    result = await db.execute(select(Object).where(Object.id == object_id))
    object_to_delete = result.scalars().first()
    if not object_to_delete:
        raise HTTPException(status_code=404, detail="Nie znaleziono obiektu o podanym id")

    result_res = await db.execute(select(Reservations).where(Reservations.object_id == object_id).where(Reservations.date >= date.today()))
    reservations = result_res.scalars().all()
    if reservations:
        raise HTTPException(status_code=409, detail="Nie można usunąć obiektu do którego przypisane są aktywne rezerwacje")

    await db.delete(object_to_delete)
    
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany danych obiektu")
    
    return {"ok": True}
    
    


    
    
    
    