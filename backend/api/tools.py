from datetime import date, datetime
from api.schemas import TableFullDTO
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria
from api.user import get_current_user
from api.schemas import HEADERS
from api.excel import generete_excel
from db.database import get_db, AsyncSessionLocal
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups, Users
from fastapi.responses import RedirectResponse, StreamingResponse
from io import BytesIO
from typing import Dict
from pdf import create_docx


router = APIRouter(prefix="/api/tools", tags=["tools"])
async def get_docx(payload: Dict):
    docx = create_docx(payload['data'], payload['comment'], payload['date'])
    return Response(
        content=docx,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": 'attachment; filename="raport.docx"'
        }
    )
