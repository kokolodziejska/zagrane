from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List

from db.database import get_db
from fastapi import APIRouter, HTTPException
from db.models import Reservations
from db.models import Price
from db.models import Global


from pydantic import BaseModel
import json

from sqlalchemy.exc import IntegrityError

import jwt
import os
from datetime import time, date, datetime, timedelta


SECRET_KEY = os.getenv("JWT_SECRET", "jakis-ciag-znakow")   ## w wersji produkcyjnej do zmiany na os.environ["JWT_SECRET"]
ALGORITHM = "HS256"



def decode_access_token(token: str) ->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def parse_time(hhmm: str) -> time: 
    h, m = hhmm.split(":")
    return time(hour=int(h),minute=int(m))

def add_minutes(t: time, mins: int) -> time:
    dt = datetime.combine(datetime.min.date(), t) + timedelta(minutes=mins)
    return dt.time()

def t_to_min(t: time) -> int:
    return t.hour * 60 + t.minute

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

router = APIRouter(prefix="/api/reservations", tags=["reservations"])

class ToCalculate(BaseModel):
    objectId: int
    date: date
    start: time
    duration: int
    split: bool
    players: int
    acceptedRules: bool

class PriceCalcResponse(BaseModel):
    total: float
    perUser: float
    currency: str

def _decode_user_id_from_cookie(access_token: str) -> int:
    if not access_token:
        raise HTTPException(status_code=401, detail="Brak tokenu")
    try:
        payload = decode_access_token(access_token)
        sub = payload.get("sub")
        user_id = int(sub)  # bezpieczne rzutowanie
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    return user_id
    
@router.post("/calc_price", response_model=PriceCalcResponse)
async def calc_price_of_reservation(calc_price: ToCalculate, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
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
    
    try:
        client_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    
    day_of_week = calc_price.date.weekday() ##od 0-6
    mask = 1 << day_of_week ##przeuń w lewo o n pozycji w zapisie binarnym
    
    res_start = calc_price.start
    res_end   = add_minutes(calc_price.start, calc_price.duration)

    price_stmt = (
        select(Price)
        .where(
            (Price.object_id == calc_price.objectId)
            &(Price.valid_from <= calc_price.date)
            &(Price.valid_to >= calc_price.date)
            &(Price.day_mask.op('&')(mask) != 0)
            &(Price.start_hour < res_end)
            &(Price.end_hour > res_start)
        )
        .order_by(Price.start_hour, Price.end_hour)
    )
    result = await db.execute(price_stmt) ##ogranicza nas tylko do przedziałów na które nachodzi rezerwacja
    rules = result.scalars().all()
    
    total = 0.0
    if len(rules) == 0:
        raise HTTPException(status_code=501, detail="Błąd obliczania ceny")
    elif len(rules) == 1:
        total = (rules[0].price/rules[0].duration)*(calc_price.duration/60)
    else:
        curr_start = t_to_min(res_start)
        curr_end = curr_start + calc_price.duration
        
        for r in rules:
            r_start = t_to_min(r.start_hour)
            r_end = t_to_min(r.end_hour)
            
            seg_start=max(r_start,curr_start)
            seg_end=min(curr_end, r_end)
            gap = (seg_end - seg_start)
            
            if(gap>0):
                total = total + ((gap/60) * (r.price/r.duration))
                curr_start = r_end
            if curr_start>=curr_end:
                break
    
    currency = rules[0].currency
    if calc_price.split:
        if calc_price.players <= 0:
            raise HTTPException(status_code=422, detail="Nieprawidłowa liczba graczy")
        per_user = total / calc_price.players
    else:
        per_user = total
        
    return {"total": round(total, 2), "perUser": round(per_user, 2), "currency": currency}
 
class NewReservation(BaseModel):
    objectId: int
    date: date
    start: time
    duration: int
    split: bool
    players: int
    acceptedRules: bool
    total: float
    userTotal: float
    
@router.post("/new_reservation", status_code=201)   
async def add_new_reservation(new_reservation: NewReservation, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    
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
    
    try:
        client_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Niepoprawny token")

    
    make_new = Reservations(
        client_id = client_id,
        object_id = new_reservation.objectId,
        date = new_reservation.date,
        hour = new_reservation.start,
        duration = new_reservation.duration,
        split = new_reservation.split,
        players = new_reservation.players,
        accepted_rule = new_reservation.acceptedRules,
        total = new_reservation.total,
        user_total = new_reservation.userTotal,
    )
    
    db.add(make_new)
    await db.flush()
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zapisu rezerwacji")
    
    return {"response": "reservation made", "id": make_new.id}
    
    
@router.get("/user_resevations_actual", response_model=List[dict])
async def get_user_reservations_actual(db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):

    user_id = _decode_user_id_from_cookie(access_token)
    
    result = await db.execute(select(Reservations).where(Reservations.client_id == user_id).where(Reservations.date >= date.today()))
    reservations = result.scalars().all()
    return [
        {
            "id": r.id,
            "client_id": r.client_id,
            "object_id": r.object_id,
            "date": r.date,
            "hour": r.hour.strftime("%H:%M"),
            "duration": r.duration,            
        }
        for r in reservations
    ]

@router.get("/user_resevations_history", response_model=List[dict])
async def get_user_reservations_history(db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):

    user_id = _decode_user_id_from_cookie(access_token)
    
    result = await db.execute(select(Reservations).where(Reservations.client_id == user_id).where(Reservations.date < date.today()))
    reservations = result.scalars().all()
    return [
        {
            "id": r.id,
            "client_id": r.client_id,
            "object_id": r.object_id,
            "date": r.date,
            "hour": r.hour.strftime("%H:%M"),
            "duration": r.duration,            
        }
        for r in reservations
    ]

    
@router.get("/", response_model=List[dict])
async def get_reservations(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Reservations))
    reservations = result.scalars().all()
    return [
        {
            "id": r.id,
            "client_id": r.client_id,
            "object_id": r.object_id,
            "date": r.date,
            "hour": r.hour.strftime("%H:%M"),
            "duration": r.duration,            
        }
        for r in reservations
    ]

@router.get("/for_day", response_model=List[dict])
async def get_reservations_day_path(day: date, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Reservations).where(Reservations.date == day).order_by(Reservations.object_id, Reservations.hour)
    )
    reservations = result.scalars().all()
    return [
        {
            "id": r.id,
            "client_id": r.client_id,
            "object_id": r.object_id,
            "date": r.date,
            "hour": r.hour.strftime("%H:%M"),
            "duration": r.duration,
        }
        for r in reservations
    ]

@router.get("/for_day_for_object", response_model=List[dict])
async def get_reservations_day_path(day: date, id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Reservations).where(Reservations.date == day, Reservations.object_id == id ).order_by(Reservations.hour)
    )
    
    reservations = result.scalars().all()
    return [
        {
            "id": r.id,
            "client_id": r.client_id,
            "object_id": r.object_id,
            "date": r.date,
            "hour": r.hour.strftime("%H:%M"),
            "duration": r.duration,
        }
        for r in reservations
    ]
@router.delete("/delate/{res_id}")
async def delete_object(res_id: int, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
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
    
    result = await db.execute(select(Reservations).where(Reservations.id == res_id))
    object_to_delete = result.scalars().first()
    if not object_to_delete:
        raise HTTPException(status_code=404, detail="Nie znaleziono reezrwacji o podanym id")

    glob_res = await db.execute(select(Global))
    glob = glob_res.scalars().first()
    if not glob:
        raise HTTPException(status_code=404, detail="Global settings not found") 

    try:
        reservation_start = datetime.combine(object_to_delete.date, object_to_delete.hour)
    except Exception:
        raise HTTPException(status_code=500, detail="Błędny format daty/godziny rezerwacji")

    min_hours_raw = getattr(glob, "min_cancel_time", getattr(glob, "minCacncelTime", 0)) or 0
    min_hours = float(min_hours_raw)
    deadline = reservation_start - timedelta(seconds=int(min_hours * 3600))

    now = datetime.now()  

    if now > deadline:
        raise HTTPException(
            status_code=400,
            detail=f"Rezerwację można odwołać najpóźniej {min_hours:.0f} h przed rozpoczęciem.",
        )
    if now >= reservation_start:
        raise HTTPException(
            status_code=400,
            detail="Nie można odwołać rozpoczętej lub zakończonej rezerwacji.",
        )

    await db.delete(object_to_delete)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany danych rezerwacji")

    return {"ok": True}

@router.delete("/admin_delate/{res_id}")
async def delete_object(res_id: int, db: AsyncSession = Depends(get_db), access_token: str = Cookie(None)):
    token = require_token(access_token)
    role = token.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Brak uprawnień")
    
    result = await db.execute(select(Reservations).where(Reservations.id == res_id))
    object_to_delete = result.scalars().first()
    if not object_to_delete:
        raise HTTPException(status_code=404, detail="Nie znaleziono reezrwacji o podanym id")
    if not object_to_delete.date<date.today():
        raise HTTPException(status_code=404, detail="Nie można odwołać rezerwacji, któa się już odbyła")


    await db.delete(object_to_delete)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Błąd zmiany danych rezerwacji")

    return {"ok": True}