from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.database import get_db
from fastapi import APIRouter, HTTPException
from db.models import Price
from db.models import PriceConfig

from datetime import time
from config.price_config import PriceConfigSchema

router = APIRouter(prefix="/api/prices", tags=["prices"])

@router.get("/", response_model=List[dict])
async def get_prices(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Price).order_by(Price.price_table).order_by(Price.object_id).order_by(Price.day_mask).order_by(Price.start_hour))
    prices = result.scalars().all()
    return [
    {
        "id": p.id,
        "price_table": p.price_table,
        "object_id": p.object_id,
        "valid_from": p.valid_from,
        "valid_to": p.valid_to, 
        "day_mask": p.day_mask,
        "start_hour": p.start_hour.strftime("%H:%M"),
        "end_hour": p.end_hour.strftime("%H:%M"),
        "duration": p.duration,  
        "price": float(p.price),
        "price_with_pass": float(p.price_with_pass) if p.price_with_pass is not None else None,
    }
    for p in prices
]

@router.get("/price_table", response_model=List[PriceConfigSchema])
async def get_price_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PriceConfig))
    rows = result.scalars().all()

    return [PriceConfigSchema.model_validate(r.config) for r in rows]



    
    
    