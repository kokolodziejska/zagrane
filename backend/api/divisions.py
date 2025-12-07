from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.database import get_db
from db.models import Chapters, Divisions
from api.schemas import ChapterRead, DivisionRead 

router = APIRouter(prefix="/api/divisions", tags=["Divisions"])

@router.get(
    "/",
    response_model=List[DivisionRead],
    summary="Get all Divisions"
)
async def get_divisions(
    db: AsyncSession = Depends(get_db)
) -> List[DivisionRead]:
    stmt = select(Divisions)
    result = await db.execute(stmt)
    divisions_orm = result.scalars().all()

    return [DivisionRead.model_validate(d) for d in divisions_orm]

@router.get(
    "/{division_id}/chapters",
    response_model=List[ChapterRead],
    summary="Get all Chapters for a specific Division"
)
async def get_chapters_by_division(
    division_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[ChapterRead]:
    division = await db.get(Divisions, division_id)
    if not division:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Division with ID {division_id} not found"
        )

    stmt = select(Chapters).where(Chapters.division_id == division_id).order_by(Chapters.value)
    result = await db.execute(stmt)
    chapters_orm = result.scalars().all()

    return [ChapterRead.model_validate(c) for c in chapters_orm]
