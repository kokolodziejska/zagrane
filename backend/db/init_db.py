import asyncio
from datetime import time, date
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from passlib.hash import argon2

from .database import engine, Base, AsyncSessionLocal
from .models import (
    Authentication, Tasks, Users, Departments, UserTypes, Tables, 
    Statuses, DepartmentTables, Rows, Divisions, Chapters, 
    Paragraphs, ExpenseGroups, RowDatas
)

async def init_db():
    print("--- Starting Database Initialization ---")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("Schema recreated successfully.")

    async with AsyncSessionLocal() as session:
        try:
            this_year = date.today().year;

            u_type = UserTypes(type="admin")
            session.add(u_type)
            
            dept = Departments(type="Departament A")
            session.add(dept)
            
            task_full = Tasks(value="22.1.1.1", type="action", description="Koordynacja działalności oraz obsługa administracyjna i techniczna")
            session.add(task_full)
            task = Tasks(value="22.1", type="task", description="Koordynacja działalności oraz obsługa administracyjna i techniczna")
            session.add(task)
            
            stat = Statuses(value="Active")
            session.add(stat)
            
            exp_group = ExpenseGroups(definition="wydatki bieżące jednostek budżetowych")
            session.add(exp_group)
            
            div = Divisions(value="750")
            session.add(div)
            
            table = Tables(year=this_year, version="v1.0", isOpen=True, budget=Decimal("1000000.00"))
            session.add(table)

            hashed_pw = argon2.hash("123") 
            auth = Authentication(password=hashed_pw) 
            session.add(auth)

            await session.flush()

            user = Users(
                auth_id=auth.user_id,
                user_name="admin",
                name="John",
                surname="Doe",
                department_id=dept.id,
                user_type_id=u_type.id
            )
            session.add(user)

            chapter = Chapters(
                division_id=div.id,
                value="75001"
            )
            session.add(chapter)

            dept_table = DepartmentTables(
                table_id=table.id,
                department_id=dept.id,
                status_id=stat.id,
                start=time(8, 0),
                end=time(16, 0)
            )
            session.add(dept_table)

            await session.flush()

            paragraph = Paragraphs(
                chapter_id=chapter.id,
                expense_group_id=exp_group.id,
                value="400"
            )
            session.add(paragraph)

            row = Rows(
                department_table_id=dept_table.id,
                last_update=time(12, 0),
                next_year=False
            )
            session.add(row)

            await session.flush()

            row_data = RowDatas(
                row_id=row.id,
                last_user_id=user.id,
                last_update=time(12, 30),
                
                budget_part="1",
                division_id=div.id,
                chapter_id=chapter.id,
                paragraph_id=paragraph.id,
                expense_group_id=exp_group.id,
                
                task_budget_full=task_full,
                task_budget_function=task,
                funding_source="D3",
                budget_code="WB27.BP.PF",

                
                financial_needs_0=Decimal("5"),
                expenditure_limit_0=Decimal("2"),
                unallocated_task_funds_0=Decimal("3"),
                contract_amount_0=Decimal("1"),
                contract_number_0="Nie dotyczy",

                
                financial_needs_1=Decimal("5"),
                expenditure_limit_1=Decimal("5"),
                unallocated_task_funds_1=Decimal("0"),
                contract_amount_1=Decimal("1"),
                contract_number_1="Nie dotyczy",


                financial_needs_2=Decimal("5"),
                expenditure_limit_2=Decimal("4"),
                unallocated_task_funds_2=Decimal("1"),
                contract_amount_2=Decimal("1"),
                contract_number_2="Nie dotyczy",


                financial_needs_3=Decimal("5"),
                expenditure_limit_3=Decimal("2"),
                unallocated_task_funds_3=Decimal("3"),
                contract_amount_3=Decimal("1"),
                contract_number_3="Nie dotyczy",

                
                task_name="audyt bezpieczeństwa informacji zgodnie z normą ISO 27001",
                task_justification="audyt bezpieczeństwa informacji zgodnie z normą ISO 27001",
                expenditure_purpose="koszty funkcjonowania",
                notes="Initial Seed Data"
            )
            session.add(row_data)

            await session.commit()
            print("--- Data Seeding Complete: All tables populated ---")

        except Exception as e:
            print(f"!!! Error during seeding: {e}")
            await session.rollback()
            raise e

if __name__ == "__main__":
    asyncio.run(init_db())