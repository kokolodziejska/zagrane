from api.schemas import TableFullDTO, DepartmentRead
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria
from typing import List
from api.schemas import HEADERS
from api.excel import generete_excel
from db.database import get_db, AsyncSessionLocal
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups, Departments
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter(prefix="/api/departments", tags=["departments"])

@router.get("/get_all_departments")
async def get_all_department_names(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Departments))
    departments = result.scalars().all()

    return set([dep.type for dep in departments])

@router.get("/get_department_dates")
async def get_department_dates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DepartmentTables))
    dept_tables = result.scalars().all()

    output = []

    for dt in dept_tables:
        dep_result = await db.execute(
            select(Departments).where(Departments.id == dt.department_id)
        )
        department = dep_result.scalars().first()

        output.append([
            department.type if department else None,
            dt.end,
            dt.start
        ])

    return output

