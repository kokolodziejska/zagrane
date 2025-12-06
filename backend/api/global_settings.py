from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from sqlalchemy import delete

from db.database import get_db
from fastapi import APIRouter, HTTPException
from db.models import Global
from db.models import Discipline
from sqlalchemy.orm import selectinload

from pydantic import BaseModel, Field
from pathlib import Path


import jwt
import os
from datetime import time

from sqlalchemy.exc import IntegrityError


SECRET_KEY = os.getenv("JWT_SECRET", "jakis-ciag-znakow")   ## w wersji produkcyjnej do zmiany na os.environ["JWT_SECRET"]
ALGORITHM = "HS256"

PROTECTED_DIS = "All"

router = APIRouter(prefix="/api/global_settings", tags=["global_settings"])

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


def validate_opening_hour_and_closing_hour(openingHour: time, closingHour: time)-> Optional[str]:
    if  not openingHour or not closingHour:
        return "Godziny otwarcia i zamknięcia są wymagane"
    if closingHour < openingHour:
        return "Godzina zamknięcia nie może być wcześniejsza niż godzina otwarcia"

    return None


def validate_timeBlock(timeBlock: float)-> Optional[str]:
    if timeBlock < 0.25:
        return "Krok musi być co najmniej 15 minut"
    if timeBlock > 2:
        return "Krok nie może przekraczać 120 minut"
    return None

def validate_minimalTimeBlock(timeBlock: float, minimalTimeBlock: float)-> Optional[str]:
    if minimalTimeBlock < timeBlock:
        return "Minimalny czas nie może być krótszy niż krok"
    if minimalTimeBlock % timeBlock != 0:
        return "Minimalny czas musi być wielokrotnością kroku"
    return None

def validate_maximalTimeBlock(timeBlock: float, minimalTimeBlock: float, maximalTimeBlock: float)-> Optional[str]:
    if minimalTimeBlock > maximalTimeBlock:
        return "Maksymalny czas musi być ≥ minimalnego"
    
    if maximalTimeBlock % timeBlock != 0:
        return "Maksymalny czas musi być wielokrotnością kroku"
    return None 

def validate_minBookingAdvanceTime(minBookingAdvanceTime: float)-> Optional[str]:
    if minBookingAdvanceTime < 0.25:
        return "Wyprzedzenie rezerwacji musi mieć wartość ≥ 15 minut"
    return None

def validate_minCancelTime(minBookingAdvanceTime: float)-> Optional[str]:
    if minBookingAdvanceTime < 2:
        return "Wyprzedzenie odwołania rezerwacji musi mieć wartość ≥ 2 h"
    return None

def validate_discypline(name: str) -> Optional[str]:
    name = name.strip()
    if len(name)<2 or len(name)>15:
        return "Dyscyplina musi mieć min. 2 znaki i max. 15 znaków"
    return None

class CompanyDefaults(BaseModel):
    openingHour: str
    closingHour: str
    
    timeBlock: float
    minimalTimeBlock: float
    maximalTimeBlock: float
    minBookingAdvanceTime: float
    
    defaultPlayers: int
    defaultDiscipline: Optional[str]
    availableDisciplines: List[str]


@router.get("/get_global_company_settings", response_model=CompanyDefaults)
async def get_global_company_settings(db: AsyncSession = Depends(get_db)):
    
    glob_res = await db.execute(select(Global))
    glob = glob_res.scalars().first()
    if not glob:
        raise HTTPException(404, "Global settings not found")
    dis_res = await db.execute(select(Discipline))
    dis = dis_res.scalars().all()
    
    return CompanyDefaults(
        openingHour=glob.opening_hour.strftime("%H:%M"),
        closingHour=glob.closing_hour.strftime("%H:%M"),
        timeBlock=float(glob.time_block),
        minimalTimeBlock=float(glob.minimal_time_block),
        maximalTimeBlock=float(glob.maximal_time_block),
        minBookingAdvanceTime=float(glob.min_booking_advance_time),
        defaultPlayers=glob.default_players,
        defaultDiscipline=(glob.default_discipline.name if glob.default_discipline else None),
        availableDisciplines=[d.name for d in dis if d.is_enabled],
    )

class FullCompanyDefaults(BaseModel):
    openingHour: str
    closingHour: str
    
    timeBlock: float
    minimalTimeBlock: float
    maximalTimeBlock: float
    minBookingAdvanceTime: float
    minCacncelTime: float
    currency: str
    
    defaultPlayers: int
    defaultDiscipline: Optional[str]
    availableDisciplines: List[str]


@router.get("/get_full_global_company_settings", response_model=FullCompanyDefaults)
async def get_full_global_company_settings(db: AsyncSession = Depends(get_db)):
    
    glob_res = await db.execute(select(Global))
    glob = glob_res.scalars().first()
    if not glob:
        raise HTTPException(404, "Global settings not found")
    dis_res = await db.execute(select(Discipline))
    dis = dis_res.scalars().all()
    
    return FullCompanyDefaults(
        openingHour=glob.opening_hour.strftime("%H:%M"),
        closingHour=glob.closing_hour.strftime("%H:%M"),
        timeBlock=float(glob.time_block),
        minimalTimeBlock=float(glob.minimal_time_block),
        maximalTimeBlock=float(glob.maximal_time_block),
        minBookingAdvanceTime=float(glob.min_booking_advance_time),
        minCacncelTime=float(glob.min_cancel_time),
        currency=glob.currency,
        defaultPlayers=glob.default_players,
        defaultDiscipline=(glob.default_discipline.name if glob.default_discipline else None),
        availableDisciplines=[d.name for d in dis if d.is_enabled],
    )

class CompanyNewData(BaseModel):
    openingHour: time
    closingHour: time
    
    timeBlock: float
    minimalTimeBlock: float
    maximalTimeBlock: float
    minBookingAdvanceTime: float
    minCacncelTime: float
    
    
@router.post("/edit_global_company_settings")
async def gedit_global_company_settings(new_data: CompanyNewData, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    
    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    error = validate_opening_hour_and_closing_hour(new_data.openingHour, new_data.closingHour)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_timeBlock(new_data.timeBlock)
    if error:
        raise HTTPException(status_code=400, detail=error)
       
    error = validate_minimalTimeBlock(new_data.timeBlock, new_data.minimalTimeBlock)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_maximalTimeBlock(new_data.timeBlock, new_data.minimalTimeBlock, new_data.maximalTimeBlock)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_minBookingAdvanceTime(new_data.minBookingAdvanceTime)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    error = validate_minCancelTime(new_data.minCacncelTime)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    result_glob = await db.execute(select(Global))
    glob = result_glob.scalars().first()
    if not glob:
        raise HTTPException(status_code=404, detail="Global settings not found")
    
    glob.opening_hour = new_data.openingHour
    glob.closing_hour = new_data.closingHour
    glob.time_block = new_data.timeBlock
    glob.minimal_time_block = new_data.minimalTimeBlock
    glob.maximal_time_block = new_data.maximalTimeBlock
    glob.min_booking_advance_time = new_data.minBookingAdvanceTime
    glob.min_cancel_time = new_data.minCacncelTime
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany globalnych danych")
    
    return {"ok": True}

class DisciplineOut(BaseModel):
    name: str
    is_enabled: bool

@router.get("/get_discyplines", response_model=List[DisciplineOut])
async def get_discyplines(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Discipline).order_by(Discipline.name))
    disc= result.scalars().all()
    return [
        {
            "name": d.name,
            "is_enabled": d.is_enabled
        }
        for d in disc
    ]
    
class DefNumberOfPlayers(BaseModel):
     defaultDiscipline: str
    
    
@router.post("/edit_default_discipline")
async def edit_default_discipline(new_data: DefNumberOfPlayers, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    
    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    
    result_glob = await db.execute(select(Global))
    glob = result_glob.scalars().first()
    if not glob:
        raise HTTPException(status_code=404, detail="Nie znaleziono takiej dyscypliny")
    
    result_dis = await db.execute(select(Discipline).where(Discipline.name == new_data.defaultDiscipline))
    discipline_obj = result_dis.scalars().first()

    if not discipline_obj:
        raise HTTPException(status_code=404, detail="Nie znaleziono takiej dyscypliny")

    glob.default_discipline = discipline_obj
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany globalnych danych")
    
    return {"ok": True}

class NewDiscipline(BaseModel):
    name: str
    
@router.post("/add_disciplines")
async def add_disciplines(new_data: NewDiscipline, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):

    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    new_data.name = new_data.name.strip()
    result = await db.execute(select(Discipline).where(Discipline.name == new_data.name))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=409, detail="Istnieje juz taka dyscyplina")
    
    dis_err = validate_discypline(new_data.name)
    if dis_err:
        raise HTTPException(status_code=400, detail=dis_err)
    
    new_dis = Discipline(
        name = new_data.name,
        is_enabled = True
    )
    
    db.add(new_dis)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu unowej sycypliny")
    
    return {"ok": True}

class ChangeDiscipline(BaseModel):
    name: str
    is_enabled: bool

class UpdateDisciplineList(BaseModel):
    disciplines: List[ChangeDiscipline]

@router.post("/update_disciplines_visibility")
async def update_disciplines_visibility(new_data: UpdateDisciplineList , db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    
    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    if not new_data.disciplines:
        raise HTTPException(status_code=400, detail="Lista dyscyplin nie może być pusta")
    
    has_all = any(d.name == PROTECTED_DIS for d in new_data.disciplines)
    if not has_all:
        raise HTTPException(status_code=400, detail=f"Lista musi zawierać dyscyplinę '{PROTECTED_DIS}'")
    
    res_glob = await db.execute(select(Global).options(selectinload(Global.default_discipline)))
    glob = res_glob.scalars().first()
    if not glob:
        raise HTTPException(status_code=404, detail="Global settings not found")
    old_name = glob.default_discipline.name

    has_def = any(d.name == old_name for d in new_data.disciplines)
    if not has_def:
        raise HTTPException(status_code=400, detail=f"Lista musi zawierać domyślną dyscyplinę '{old_name}'")
    
    await db.execute(delete(Discipline))
    db.add_all([
        Discipline(name=d.name, is_enabled=d.is_enabled)
        for d in new_data.disciplines
    ])
    await db.flush() 

    result_dis = await db.execute(select(Discipline).where(Discipline.name == old_name))
    discipline_obj = result_dis.scalars().first()

    glob.default_discipline = discipline_obj
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany widoczności dyscypliny")

    return {"ok": True} 
    
    
class DefNumberOfPlayers(BaseModel):
     players: int
    
    
@router.post("/edit_default_players_number")
async def edit_default_players_number(new_data: DefNumberOfPlayers, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    
    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    if new_data.players < 1:
        raise HTTPException(status_code=404, detail="Domyślna liczba graczy musi mieć wartosć przynajmniej 1")
    
    result_glob = await db.execute(select(Global))
    glob = result_glob.scalars().first()
    if not glob:
        raise HTTPException(status_code=405, detail="Nie znaleziono globalnych ustawień")

    glob.default_players = new_data.players
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany globalnych danych")
    
    return {"ok": True}
    
    
    
    
    
    