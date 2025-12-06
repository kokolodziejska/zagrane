from api.schemas import TableFullDTO
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from db.database import get_db
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups

router = APIRouter(prefix="/api/tables", tags=["tables"])

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