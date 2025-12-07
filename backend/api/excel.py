from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException

from api.schemas import TableFullDTO, HEADERS

from db.database import get_db
from db.models import Tables, DepartmentTables, Rows, RowDatas, Divisions, Chapters, Paragraphs, ExpenseGroups
import pandas as pd

from datetime import datetime
import os

# wczytać tabele po id tabeli
# na podstawoe danych tabeli zrobić excela

'''
by wywołać:
async with AsyncSessionLocal() as db:
    await generete_excel(1, db)
'''
def dto_to_rows(dto):
    rows = []
    for dept_table in dto.department_tables:
        for row in dept_table.rows:
            rows.append({HEADERS[i]: i for i in range(len(HEADERS))})
            for row_data in row.row_datas:
                rows.append({
                    HEADERS[0]: row_data.budget_part,
                    HEADERS[1]: row_data.division.value,
                    HEADERS[2]: row_data.chapter.value,
                    HEADERS[3]: row_data.paragraph.value,
                    HEADERS[4]: row_data.funding_source,
                    HEADERS[5]: row_data.expense_group.definition,
                    HEADERS[6]: row_data.task_budget_full.value,
                    HEADERS[7]: row_data.task_budget_function.value,
                    HEADERS[8]: row_data.program_project_name,
                    HEADERS[9]: row_data.organizational_unit_name,
                    HEADERS[10]: row_data.plan_wi,
                    HEADERS[11]: row_data.fund_distributor,
                    HEADERS[12]: row_data.budget_code,
                    HEADERS[13]: row_data.task_name,
                    HEADERS[14]: row_data.task_justification,
                    HEADERS[15]: row_data.expenditure_purpose,

                    HEADERS[16]: row_data.financial_needs_0,
                    HEADERS[17]: row_data.expenditure_limit_0,
                    HEADERS[18]: row_data.unallocated_task_funds_0,
                    HEADERS[19]: row_data.contract_amount_0,
                    HEADERS[20]: row_data.contract_number_0,
                 
                    HEADERS[21]: row_data.financial_needs_1,
                    HEADERS[22]: row_data.expenditure_limit_1,
                    HEADERS[23]: row_data.unallocated_task_funds_1,
                    HEADERS[24]: row_data.contract_amount_1,
                    HEADERS[25]: row_data.contract_number_1,
                 
                    HEADERS[26]: row_data.financial_needs_2,
                    HEADERS[27]: row_data.expenditure_limit_2,
                    HEADERS[28]: row_data.unallocated_task_funds_2,
                    HEADERS[29]: row_data.contract_amount_2,
                    HEADERS[30]: row_data.contract_number_2,
                 
                    HEADERS[31]: row_data.financial_needs_3,
                    HEADERS[32]: row_data.expenditure_limit_3,
                    HEADERS[33]: row_data.unallocated_task_funds_3,
                    HEADERS[34]: row_data.contract_amount_3,
                    HEADERS[35]: row_data.contract_number_3,

                    HEADERS[36]: row_data.subsidy_agreement_party,
                    HEADERS[37]: row_data.legal_basis_for_subsidy,
                    HEADERS[38]: row_data.notes,
                })
            rows.append({HEADERS[i]: None for i in range(len(HEADERS))})
    return rows

async def generete_excel(table_id: int, db: AsyncSession = Depends(get_db)):
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
    print(dto.model_dump_json())
    rows = dto_to_rows(dto)
    df = pd.DataFrame(rows)

    return df
