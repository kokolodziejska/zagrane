from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.database import get_db
from db.models import Paragraphs, Chapters
from api.schemas import ParagraphRead 

router = APIRouter(prefix="/api/chapters", tags=["Chapters"])

@router.get(
    "/{chapter_id}/paragraphs",
    response_model=List[ParagraphRead],
    summary="Get all Paragraphs for a specific Chapter"
)
async def get_paragraphs_by_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db)
) -> List[ParagraphRead]:
    chapter = await db.get(Chapters, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Chapter with ID {chapter_id} not found"
        )

    stmt = select(Paragraphs).where(Paragraphs.chapter_id == chapter_id).order_by(Paragraphs.value)
    result = await db.execute(stmt)
    paragraphs_orm = result.scalars().all()

    return [ParagraphRead.model_validate(p) for p in paragraphs_orm]