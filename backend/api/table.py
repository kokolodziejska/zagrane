from api.schemas import TableFullDTO
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List
from api.schemas import HEADERS
from api.excel import generete_excel
from db.database import get_db, AsyncSessionLocal
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter(prefix="/api/tables", tags=["tables"])

@router.get("/{table_id}/generate_spreadsheet")
async def get_excel(table_id: int):
    async with AsyncSessionLocal() as db:
        df = await generete_excel(table_id, db)

    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data to generate Excel")

    stream = BytesIO()
    df.to_excel(stream, index=False, engine='openpyxl')
    stream.seek(0)
    
    return StreamingResponse(
        stream,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename=table_{table_id}.xlsx"}
    )
    

@router.get("/headers", response_model=List[str])
async def get_table_headers():
    return HEADERS

@router.get("/{table_id}", response_model=TableFullDTO)
async def get_table_hierarchy(table_id: int, db: AsyncSession = Depends(get_db)):
    query = (
        select(Tables)
        .where(Tables.id == table_id)
        .options(
            selectinload(Tables.department_tables).options(
                joinedload(DepartmentTables.department),
                joinedload(DepartmentTables.status),
                
                selectinload(DepartmentTables.rows).options(
                    selectinload(Rows.row_datas).options(
                        joinedload(RowDatas.division),
                        joinedload(RowDatas.chapter),
                        joinedload(RowDatas.paragraph),
                        joinedload(RowDatas.expense_group),
                        joinedload(RowDatas.task_budget_full),
                        joinedload(RowDatas.task_budget_function),
                    )
                )
            )
        )
    )

    result = await db.execute(query)
    table = result.scalars().first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    return table



