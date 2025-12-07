from api.schemas import TableFullDTO, DepartmentRead
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload, with_loader_criteria
from typing import List
from api.schemas import HEADERS, DeptLimitUpdateRequest
from api.excel import generete_excel
from db.database import get_db, AsyncSessionLocal
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups, Departments
from fastapi.responses import StreamingResponse
from io import BytesIO
from decimal import Decimal

router = APIRouter(prefix="/api/departments", tags=["departments"])

@router.put("/update_expenditure_limits")
async def update_expenditure_limits(req: DeptLimitUpdateRequest, db: AsyncSession = Depends(get_db)):
    for dept_name, new_limit in req.updates:
        result = await db.execute(select(Departments).where(Departments.type == dept_name))
        department = result.scalars().first()
        if not department:
            continue

        result = await db.execute(
            select(DepartmentTables).where(DepartmentTables.department_id == department.id)
        )
        dept_tables = result.scalars().all()

        for dt in dept_tables:
            print(1)
            result = await db.execute(select(Rows).where(Rows.department_table_id == dt.id))
            rows = result.scalars().all()

            for row in rows:
                print(2)
                result = await db.execute(select(RowDatas).where(RowDatas.row_id == row.id))
                row_datas = result.scalars().all()

                for rd in row_datas:
                    print(3)
                    rd.expenditure_limit_0 = Decimal(new_limit)
                    db.add(rd)
                    await db.flush()        # ensure SQL is executed
                    await db.refresh(rd) 
                    
    await db.commit()
    return {"status": "success"}

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

