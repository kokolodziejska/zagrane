from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from db.database import get_db
from db.models import Paragraphs, Chapters
from api.schemas import ParagraphRead 

router = APIRouter(prefix="/api/chapters", tags=["Chapters"])

@router.get(
    "/{chapter_value}/paragraphs",
    response_model=List[ParagraphRead],
    summary="Get all Paragraphs for a specific Chapter"
)
async def get_paragraphs_by_chapter(
    chapter_value: str,
    db: AsyncSession = Depends(get_db)
) -> List[ParagraphRead]:
    stmt = select(Chapters).where(Chapters.value == chapter_value)
    result = await db.execute(stmt)
    chapter = result.scalars().first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Chapter with ID {chapter_value} not found"
        )

    stmt = (
        select(Paragraphs)
        .options(
            selectinload(Paragraphs.expense_group)
        )
        .where(Paragraphs.chapter_id == chapter.id)
        .order_by(Paragraphs.value)
    )

    result = await db.execute(stmt)
    paragraphs_orm = result.scalars().all()
    return [ParagraphRead.model_validate(p) for p in paragraphs_orm]