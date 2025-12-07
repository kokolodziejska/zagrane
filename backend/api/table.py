from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from api.schemas import TableFullDTO, BudgetUpdateRequest
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
from typing import List
from dateutil import parser

router = APIRouter(prefix="/api/tables", tags=["tables"])

@router.put("/{table_id}/update_budget")
async def update_table_budget(
    table_id: int,
    req: BudgetUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Tables).where(Tables.id == table_id))
    table = result.scalars().first()

    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    table.budget = req.budget

    db.add(table)
    await db.commit()
    await db.refresh(table)

    return {"id": table.id, "budget": str(table.budget)}


@router.get("/{table_id}/get_total_budget")
async def get_limits_per_department(table_id: int, db: AsyncSession = Depends(get_db)):
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
    dto = TableFullDTO.model_validate(table)
        
    return dto.budget

@router.get("/{table_id}/get_limits_per_department")
async def get_limits_per_department(
    table_id: int,
    db: AsyncSession = Depends(get_db),
):
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
                ),
            )
        )
    )

    result = await db.execute(query)
    table = result.scalars().first()
    if table is None:
        return {}

    dto = TableFullDTO.model_validate(table)

    sums_per_dept: dict[str, float] = {}

    for dept_table in dto.department_tables:
        dept_key = dept_table.department.type  # z modelu Departments

        # 1. Zgrupuj wiersze po row.id i wybierz najnowszy Row po last_update
        latest_rows_by_id: dict[int, any] = {}
        for row in dept_table.rows:
            existing = latest_rows_by_id.get(row.id)
            if existing is None or row.last_update > existing.last_update:
                latest_rows_by_id[row.id] = row

        partial_sum = 0.0

        # 2. Dla każdego "najnowszego" Row wybierz najnowsze RowDatas
        for row in latest_rows_by_id.values():
            if not row.row_datas:
                continue

            newest_row_data = max(
                row.row_datas,
                key=lambda rd: rd.last_update,
            )

            value = newest_row_data.expenditure_limit_0 or 0
            partial_sum += float(value)
            break

        if dept_key in sums_per_dept:
            # sums_per_dept[dept_key] += partial_sum
            pass
        else:
            sums_per_dept[dept_key] = partial_sum

    return sums_per_dept

@router.get("/{table_id}/get_needs_per_department")
async def get_needs_per_department(table_id: int, db: AsyncSession = Depends(get_db)):
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
    dto = TableFullDTO.model_validate(table)

    sums_per_dept = {}
    for dept_table in dto.department_tables:
        id = dept_table.department.type
        partial = 0
        for row in dept_table.rows:
            for row_data in row.row_datas:
                value = row_data.financial_needs_0 or 0
                partial += int(value)
        if id in sums_per_dept:
            sums_per_dept[id] += partial
        else:
            sums_per_dept[id] = partial
        
    return sums_per_dept

@router.get("/{table_id}/departments/{department_id}")
async def get_department_from_table(table_id: int, department_id: int, db: AsyncSession = Depends(get_db)):
    query = (
        select(Tables)
        .where(Tables.id == table_id)
        .options(
            with_loader_criteria(
                DepartmentTables,
                DepartmentTables.department_id == department_id,
                include_aliases=True
            ),

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
    dto = TableFullDTO.model_validate(table)
    return dto

@router.get("/{table_id}/departments/{department_id}/endDate")
async def get_department_end_date(
    table_id: int, 
    department_id: int, 
    db: AsyncSession = Depends(get_db)
) -> datetime:
    stmt = (
        select(DepartmentTables.end)
        .where(
            DepartmentTables.table_id == table_id,
            DepartmentTables.department_id == department_id
        )
    )
    
    result = await db.execute(stmt)
    end_date = result.scalar_one_or_none()

    if end_date is None:
        raise HTTPException(status_code=404, detail="Department entry not found")

    return end_date

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
async def get_table_hierarchy(
    table_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    if current_user.user_type.type != "admin":
        if not current_user.department_id:
            raise HTTPException(status_code=403, detail="User has no assigned department")
        
        return RedirectResponse(
            url=f"/api/tables/{table_id}/departments/{current_user.department_id}", 
            status_code=307
        )

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





