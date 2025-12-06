import json
from pathlib import Path
from datetime import time, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .database import engine, Base, AsyncSessionLocal
from .models import Object
from .models import Price
from .models import PriceConfig
from .models import Clients
from .models import UserAuth
from .models import Global
from .models import Discipline
from .database import get_db

import os
from passlib.hash import argon2
from config.price_config import PriceConfigSchema

SECRET_KEY = os.getenv("JWT_SECRET", "jakis-ciag-znakow")   ## w wersji produkcyjnej do zmiany na os.environ["JWT_SECRET"]
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return argon2.hash(password)

def parse_time(hhmm: str) -> time: 
    h, m = hhmm.split(":")
    return time(hour=int(h),minute=int(m))

def parse_date(iso: str) -> date:
    return date.fromisoformat(iso)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
       
        # ===  ADMIN ===
        seed_admin = os.getenv("SEED_ADMIN_ON_START")
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if seed_admin:
            if not admin_email or not admin_password:
                print("Brak danych logowania admina!!")
            else:
                admin_email =admin_email.lower().strip()
                result = await session.execute(select(Clients).where(Clients.mail == admin_email))
                existing = result.scalars().first()
                admin_result = await session.execute(select(UserAuth).where(UserAuth.role == "admin"))
                admin_existing = admin_result.scalars().first()
                if not existing and not admin_existing:
                    admin = Clients(
                        mail = admin_email,
                        name = "admini",
                        surname = "admin"
                    )
                    session.add(admin)
                    await session.flush()
                
                    new_password_hash = hash_password(admin_password)
                    new_user_auth = UserAuth (client_id = admin.id, password_hash = new_password_hash, role="admin", is_active=True,)
                    session.add(new_user_auth)
                    await session.commit()
                    print(f"[ADMIN SEED] utworzono admina: {admin_email}")
                else:
                    print("Admin już istnije, lub podoano złe dane")
        else: 
            print("Nie tworze admina")
        
         # ===  Globalne  ===
        exists = await session.scalar(select(func.count()).select_from(Global))
        exists_dis = await session.scalar(select(func.count()).select_from(Discipline))
        if ((exists or 0) + (exists_dis or 0)) > 0:
            print("global settings: already in database")
        else:
             global_path = Path(__file__).resolve().parents[1] / "setup/companyObjectsGlobal.json"
             if not global_path.exists():
                print("Brak pliku companyObjectsGlobal.json")
             else:
                data = json.loads(global_path.read_text(encoding="utf-8"))
                disc_objs = []
                for  name in data["availableDisciplines"]:
                    new_d=Discipline(name=name, is_enabled=True)
                    session.add(new_d)
                    disc_objs.append(new_d)
                    
                await session.flush()
                
                def_dis= next((d for d in disc_objs if d.name == data["defaultDiscipline"]), disc_objs[0])
                
                new_g = Global(
                    opening_hour=time.fromisoformat(data["openingHour"]),
                    closing_hour=time.fromisoformat(data["closingHour"]),
                    time_block=data["timeBlock"],
                    minimal_time_block=data["minimalTimeBlock"],
                    maximal_time_block=data["maximalTimeBlock"],
                    min_cancel_time=data["mincancelReservationTime"],
                    currency=data["currency"],
                    min_booking_advance_time=data["minBookingAdvanceTime"],
                    default_players=data["defaultPlayers"],
                    default_discipline=def_dis, 
                )
                session.add(new_g)
                await session.commit()

        # ===  Obiekty  ===
        exists = await session.scalar(select(func.count()).select_from(Object))
        if (exists or 0) > 0:
            print("objects: already in database")
        else:
            objects_path = Path(__file__).resolve().parents[1] / "setup/companyObjects.json"
            
            if not objects_path.exists():
                print("Brak pliku companyObjects.json")
            else:
                data= json.loads(objects_path.read_text(encoding="utf-8"))
                objects = data.get("objects", [])
                
                for obj in objects:
                    new = Object(
                        id=obj["id"],
                        name=obj["name"],
                        discipline = obj["discipline"],
                        description=obj.get("description"),
                        opening_hour=parse_time(obj["openingHour"]),
                        closing_hour=parse_time(obj["closingHour"]),
                        time_block=float(obj["timeBlock"]),
                        minimal_time_block=float(obj["minimalTimeBlock"]),
                        maximal_time_block=float(obj["maximalTimeBlock"]),
                    )
                    session.add(new)
                
                await session.commit()
                
         # ===  Ceny ===
        exist_pcf = await session.scalar(select(func.count()).select_from(Price))
        if (exist_pcf or 0) > 0:
            print("Prices: already in database")
        else:
            price_path = Path(__file__).resolve().parents[1] / "setup/price.json"
            
            if not price_path.exists():
                print("Brak pliku price.json")
            else:
                price_cof_data= json.loads(price_path.read_text(encoding="utf-8"))
                price_conf = price_cof_data.get("prices", [])
                
                for pr in price_conf:
                    new = Price(
                        object_id=pr["object_id"],
                        price_table=pr["table"],
                        valid_from=parse_date(pr["valid_from"]),
                        valid_to=parse_date(pr["valid_to"]),
                        day_mask=int(pr["day_mask"]),
                        start_hour=parse_time(pr["start_hour"]),
                        end_hour=parse_time(pr["end_hour"]),
                        duration=int(pr["duration"]),
                        price=float(pr["price"]),
                        price_with_pass=float(pr["price_with_pass"]) if pr.get("price_with_pass") is not None else None,
                        currency=pr["currency"],
                    )
                    session.add(new)
            
                await session.commit()

        # ===  Ceny tabela ===
        exist_pcf = await session.scalar(select(func.count()).select_from(PriceConfig))
        if (exist_pcf or 0) > 0:
            print("Price Config: already in database")
        else:
            price_path = Path(__file__).resolve().parents[1] / "setup/priceTable.json"
            
            if not price_path.exists():
                print("Brak pliku priceTable.json")
            else:
                price_conf_data = json.loads(price_path.read_text(encoding="utf-8"))
                configs_raw = price_conf_data if isinstance(price_conf_data, list) else [price_conf_data]

                configs: list[PriceConfigSchema] = []
                for item in configs_raw:
                    try:
                        cfg = PriceConfigSchema.model_validate(item)
                        configs.append(cfg)
                    except Exception as e:
                        print(f"[ERROR] Wrong JSON in priceTable.json: {e}")

                for cfg in configs:
                    session.add(PriceConfig(config=cfg.model_dump(mode="json")))

                await session.commit()
                print(f"PriceConfigs: inserted {len(configs)} row(s)")
            
                
