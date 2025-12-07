from api.schemas import TableFullDTO
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List

HEADERS = [
    "Część budżetowa",
    "Dział",
    "Rozdział",
    "Paragraf",
    "Źródło finansowania",
    "Grupa wydatków",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie publicznego",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",
    "Potrzeby finansowe na rok 2029",
    "Limit wydatków na rok 2029",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie publicznego",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",
    "Budżet zadaniowy (w pełnej szczegółowości)",
    "Budżet zadaniowy (nr funkcji, nr zadania)",
    "Nazwa programu/projektu",
    "W przypadku dotacji - z kim zawarta umowa/planowana do zawarcia umowa",
    "Nazwa komórki organizacyjnej",
    "Podstawa prawna udzielenia dotacji",
    "Plan WI",
    "Dysponent środków",
    "Budżet",
    "Nazwa zadania",
    "Szczegółowe uzasadnienie realizacji zadania",
    "Przeznaczenie wydatków wg obszaru działalności: cyberbezpieczeństwo/sztuczna inteligencja/koszty funkcjonowania/inne (wpisać jakie?)",
    "Potrzeby finansowe na rok 2026",
    "Limit wydatków na rok 2026",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie publicznego",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",
    "Potrzeby finansowe na rok 2027",
    "Limit wydatków na rok 2027",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie publicznego",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",
    "Potrzeby finansowe na rok 2028",
    "Limit wydatków na rok 2028",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie publicznego",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego"
]

from db.database import get_db
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups

router = APIRouter(prefix="/api/tables", tags=["tables"])

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



