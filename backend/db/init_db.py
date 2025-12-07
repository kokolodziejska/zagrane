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
            await seed(session)
        except Exception as e:
            print(f"!!! Error during seeding: {e}")
            await session.rollback()
            raise e

if __name__ == "__main__":
    asyncio.run(init_db())


async def seed(session):
    try:
        this_year = date.today().year

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

        await session.flush()

        # --- 3. First Row and Data ---
        row_1 = Rows(
            department_table_id=dept_table.id,
            last_update=time(12, 0),
            next_year=False
        )
        session.add(row_1)
        await session.flush() 

        row_data_1 = RowDatas(
            row_id=row_1.id,
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
            financial_needs_0=Decimal("5"), expenditure_limit_0=Decimal("2"), unallocated_task_funds_0=Decimal("3"), contract_amount_0=Decimal("1"), contract_number_0="Nie dotyczy",
            financial_needs_1=Decimal("5"), expenditure_limit_1=Decimal("5"), unallocated_task_funds_1=Decimal("0"), contract_amount_1=Decimal("1"), contract_number_1="Nie dotyczy",
            financial_needs_2=Decimal("5"), expenditure_limit_2=Decimal("4"), unallocated_task_funds_2=Decimal("1"), contract_amount_2=Decimal("1"), contract_number_2="Nie dotyczy",
            financial_needs_3=Decimal("5"), expenditure_limit_3=Decimal("2"), unallocated_task_funds_3=Decimal("3"), contract_amount_3=Decimal("1"), contract_number_3="Nie dotyczy",
            task_name="audyt bezpieczeństwa informacji zgodnie z normą ISO 27001",
            task_justification="audyt bezpieczeństwa informacji zgodnie z normą ISO 27001",
            expenditure_purpose="koszty funkcjonowania",
            notes="Initial Seed Data (Row 1)"
        )
        session.add(row_data_1)


        # --- 4. Second Row and Data ---
        row_2 = Rows(
            department_table_id=dept_table.id,
            last_update=time(13, 0),
            next_year=True 
        )
        session.add(row_2)
        await session.flush() 

        row_data_2 = RowDatas(
            row_id=row_2.id,
            last_user_id=user.id,
            last_update=time(13, 30),
            budget_part="1",
            division_id=div.id,
            chapter_id=chapter.id,
            paragraph_id=paragraph.id,
            expense_group_id=exp_group.id,
            task_budget_full=task_full,
            task_budget_function=task,
            funding_source="D3",
            budget_code="WB27.BP.PF",
            financial_needs_0=Decimal("15"), expenditure_limit_0=Decimal("10"), unallocated_task_funds_0=Decimal("5"), contract_amount_0=Decimal("10"), contract_number_0="Contract-002",
            financial_needs_1=Decimal("15"), expenditure_limit_1=Decimal("15"), unallocated_task_funds_1=Decimal("0"), contract_amount_1=Decimal("10"), contract_number_1="Contract-002",
            financial_needs_2=Decimal("15"), expenditure_limit_2=Decimal("5"), unallocated_task_funds_2=Decimal("10"), contract_amount_2=Decimal("10"), contract_number_2="Contract-002",
            financial_needs_3=Decimal("15"), expenditure_limit_3=Decimal("1"), unallocated_task_funds_3=Decimal("14"), contract_amount_3=Decimal("10"), contract_number_3="Contract-002",
            task_name="Wdrożenie systemu kontroli dostępu",
            task_justification="Nowy system bezpieczeństwa fizycznego",
            expenditure_purpose="cyberbezpieczeństwo",
            notes="Initial Seed Data (Row 2)"
        )
        session.add(row_data_2)


        row_3 = Rows(
            department_table_id=dept_table.id,
            last_update=time(14, 0),
            next_year=False
        )
        session.add(row_3)
        await session.flush()

        row_data_3 = RowDatas(
            row_id=row_3.id,
            last_user_id=user.id,
            last_update=time(14, 30),
            budget_part="1",
            division_id=div.id,
            chapter_id=chapter.id,
            paragraph_id=paragraph.id,
            expense_group_id=exp_group.id,
            task_budget_full=task_full,
            task_budget_function=task,
            funding_source="D3",
            budget_code="WB27.BP.PF",
            financial_needs_0=Decimal("20"), expenditure_limit_0=Decimal("20"), unallocated_task_funds_0=Decimal("0"), contract_amount_0=Decimal("0"), contract_number_0="Nie dotyczy",
            financial_needs_1=Decimal("20"), expenditure_limit_1=Decimal("20"), unallocated_task_funds_1=Decimal("0"), contract_amount_1=Decimal("0"), contract_number_1="Nie dotyczy",
            financial_needs_2=Decimal("20"), expenditure_limit_2=Decimal("20"), unallocated_task_funds_2=Decimal("0"), contract_amount_2=Decimal("0"), contract_number_2="Nie dotyczy",
            financial_needs_3=Decimal("20"), expenditure_limit_3=Decimal("20"), unallocated_task_funds_3=Decimal("0"), contract_amount_3=Decimal("0"), contract_number_3="Nie dotyczy",
            task_name="Szkolenia z zakresu RODO",
            task_justification="Obowiązkowe szkolenia dla pracowników",
            expenditure_purpose="koszty funkcjonowania",
            notes="Initial Seed Data (Row 3)"
        )
        session.add(row_data_3)

        # ====== SECOND DEPARTMENT ======

        # 1. Create second department
        dept_b = Departments(type="Departament B")
        session.add(dept_b)
        await session.flush()

        # 2. Department table for dept B
        dept_table_b = DepartmentTables(
            table_id=table.id,
            department_id=dept_b.id,
            status_id=stat.id,
            start=time(9, 0),
            end=time(17, 0)
        )
        session.add(dept_table_b)
        await session.flush()

        # 3. Row for dept B
        row_b1 = Rows(
            department_table_id=dept_table_b.id,
            last_update=time(10, 0),
            next_year=False
        )
        session.add(row_b1)
        await session.flush()

        # 4. Row data for dept B
        row_data_b1 = RowDatas(
            row_id=row_b1.id,
            last_user_id=user.id,
            last_update=time(10, 30),
            budget_part="2",
            division_id=div.id,
            chapter_id=chapter.id,
            paragraph_id=paragraph.id,
            expense_group_id=exp_group.id,
            task_budget_full=task_full,
            task_budget_function=task,
            funding_source="D4",
            budget_code="WB28.BP.PF",
            financial_needs_0=Decimal("50"), expenditure_limit_0=Decimal("40"), unallocated_task_funds_0=Decimal("10"), contract_amount_0=Decimal("20"), contract_number_0="Contract-B01",
            financial_needs_1=Decimal("50"), expenditure_limit_1=Decimal("35"), unallocated_task_funds_1=Decimal("15"), contract_amount_1=Decimal("20"), contract_number_1="Contract-B01",
            financial_needs_2=Decimal("50"), expenditure_limit_2=Decimal("30"), unallocated_task_funds_2=Decimal("20"), contract_amount_2=Decimal("20"), contract_number_2="Contract-B01",
            financial_needs_3=Decimal("50"), expenditure_limit_3=Decimal("25"), unallocated_task_funds_3=Decimal("25"), contract_amount_3=Decimal("20"), contract_number_3="Contract-B01",
            task_name="Budowa infrastruktury IT",
            task_justification="Nowa serwerownia",
            expenditure_purpose="infrastruktura",
            notes="Seed data for Department B"
        )
        session.add(row_data_b1)
        
        await session.commit()
        print("--- Data Seeding Complete: All tables populated with 3 rows ---")

    except IntegrityError:
        print("!!! Data already exists in the database. Rolling back.")
        await session.rollback()
    except Exception as e:
        print(f"!!! Fatal Error during seeding: {e}")
        await session.rollback()
        raise e