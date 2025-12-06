from __future__ import annotations
import enum

from datetime import time, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, Integer, SmallInteger, Time, Date, Numeric, Text, ForeignKey, Boolean 
from .database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text

class Object(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    discipline: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    opening_hour: Mapped[time] = mapped_column(Time, nullable=False, default=time(8, 0))
    closing_hour: Mapped[time] = mapped_column(Time, nullable=False, default=time(20, 0))

    time_block: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=1.0)
    minimal_time_block: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=1.0)
    maximal_time_block: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=4.0)

    # Object (1) -> (N) Reservations
    reservations: Mapped[list["Reservations"]] = relationship( back_populates="object", cascade="all, delete-orphan", lazy="selectin",)
    # Object (1) -> (N) Price
    prices: Mapped[list["Price"]] = relationship( back_populates="object", cascade="all, delete-orphan", lazy="selectin",)

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
    
class Clients(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mail: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(220), nullable=False)
    surname: Mapped[str] = mapped_column(String(220), nullable=False)

    # relacje: Client (1) -> (N) Reservations
    reservations: Mapped[list["Reservations"]] = relationship(
        back_populates="client",           
        cascade="all, delete-orphan",      
        lazy="selectin",
    )

    # relacja 1-1 z UserAuth
    auth: Mapped["UserAuth | None"] = relationship(
        back_populates="client",          
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class UserAuth(Base):
    __tablename__ = "authentication"

    # PK = FK → relacja 1-1 z Clients
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # relacja zwrotna do Clients.auth
    client: Mapped[Clients] = relationship(back_populates="auth", lazy="selectin")


class Reservations(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"),  index=True, nullable=False,)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"),  index=True, nullable=False,)

    date: Mapped[date] = mapped_column(Date, nullable=False)
    hour: Mapped[time] = mapped_column(Time, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=60)

    split: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    players: Mapped[int] = mapped_column(Integer, nullable=False)
    accepted_rule: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    total: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=False), nullable=False)
    user_total: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=False), nullable=False)
    
    # relacje zwrotne (N) -> (1)
    client: Mapped[Clients] = relationship(back_populates="reservations", lazy="selectin")
    object: Mapped[Object] = relationship(back_populates="reservations", lazy="selectin")
    
class Price(Base):
    __tablename__ = "prices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    price_table: Mapped[int] = mapped_column(Integer, index=True)

    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"),  index=True, nullable=False,)

    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_to: Mapped[date] = mapped_column(Date, nullable=False)
    
    day_mask: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=127)

    start_hour: Mapped[time] = mapped_column(Time, nullable=False)
    end_hour: Mapped[time] = mapped_column(Time, nullable=False)
    
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    price: Mapped[float] = mapped_column(Numeric(10, 2, asdecimal=False), nullable=False)
    price_with_pass: Mapped[float | None] = mapped_column(Numeric(10, 2, asdecimal=False), nullable=True)

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="PLN")
    
    # relacje zwrotne (N) -> (1)
    object: Mapped["Object"] = relationship(back_populates="prices", lazy="selectin")

class PriceConfig(Base):
    __tablename__ = "price_configs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))

class Discipline(Base):
    __tablename__ = "discipline"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(220), nullable=False, unique=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Global(Base):
    __tablename__ = "global"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    opening_hour: Mapped[time] = mapped_column(Time, nullable=False, default=time(8, 0))
    closing_hour: Mapped[time] = mapped_column(Time, nullable=False, default=time(20, 0))

    time_block: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=1.0)
    minimal_time_block: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=1.0)
    maximal_time_block: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=4.0)
    min_cancel_time: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=24.0)
    currency: Mapped[str] = mapped_column(String(220), nullable=False, unique=True)

    min_booking_advance_time: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=2.0)
    default_players: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    default_discipline_id: Mapped[int | None] = mapped_column(
        ForeignKey("discipline.id", ondelete="SET NULL"), nullable=True
    )
    # relacje
    default_discipline: Mapped["Discipline"] = relationship("Discipline")
