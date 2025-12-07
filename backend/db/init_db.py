import asyncio
from datetime import datetime, time, date, timedelta
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
            await seed_history_test(session)
            await seed_like_a_boss(session)
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
            start=datetime.now(),
            end= datetime.now() + timedelta(days=365)
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
            last_update=datetime.now(),
            next_year=False
        )
        session.add(row_1)
        await session.flush() 

        row_data_1 = RowDatas(
            row_id=row_1.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
            last_update=datetime.now(),
            next_year=True 
        )
        session.add(row_2)
        await session.flush() 

        row_data_2 = RowDatas(
            row_id=row_2.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
            last_update=datetime.now(),
            next_year=False
        )
        session.add(row_3)
        await session.flush()

        row_data_3 = RowDatas(
            row_id=row_3.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
        
        await session.commit()
        print("--- Data Seeding Complete: All tables populated with 3 rows ---")

    except IntegrityError:
        print("!!! Data already exists in the database. Rolling back.")
        await session.rollback()
    except Exception as e:
        print(f"!!! Fatal Error during seeding: {e}")
        await session.rollback()
        raise e
    

async def seed_history_test(session):
    print("--- Starting History Seeding ---")
    try:
        # 1. Fetch necessary dependencies (created in the previous seed function)
        # We need these Foreign Keys to exist to create a RowData
        user = (await session.execute(select(Users).where(Users.user_name == "admin"))).scalar_one_or_none()
        dept_table = (await session.execute(select(DepartmentTables))).scalars().first()
        division = (await session.execute(select(Divisions))).scalars().first()
        chapter = (await session.execute(select(Chapters))).scalars().first()
        paragraph = (await session.execute(select(Paragraphs))).scalars().first()
        exp_group = (await session.execute(select(ExpenseGroups))).scalars().first()
        task_full = (await session.execute(select(Tasks).where(Tasks.type == "action"))).scalars().first()
        task_func = (await session.execute(select(Tasks).where(Tasks.type == "task"))).scalars().first()

        if not all([user, dept_table, division, chapter, paragraph, exp_group, task_full, task_func]):
            print("!!! Missing dependencies. Please run the main 'seed()' function first.")
            return

        # 2. Create ONE single Row container
        # This represents the "Identity" of the row.
        history_row = Rows(
            department_table_id=dept_table.id,
            last_update=datetime.now(),
            next_year=False
        )
        session.add(history_row)
        await session.flush() # Flush to get history_row.id

        # 3. Create History Entry 1: OLD DATA (e.g., created 30 days ago)
        # Notice: Low budget (1000), Draft note
        date_v1 = datetime.now() - timedelta(days=30)
        row_data_v1 = RowDatas(
            row_id=history_row.id, # Points to the same row
            last_user_id=user.id,
            last_update=date_v1,   # Old Date
            
            budget_part="1",
            division_id=division.id,
            chapter_id=chapter.id,
            paragraph_id=paragraph.id,
            expense_group_id=exp_group.id,
            task_budget_full=task_full,
            task_budget_function=task_func,
            funding_source="D3",
            budget_code="WB27.HIST.TEST",
            
            # Values for Version 1
            financial_needs_0=Decimal("1000"), expenditure_limit_0=Decimal("1000"), unallocated_task_funds_0=Decimal("0"), contract_amount_0=Decimal("0"), contract_number_0="Draft",
            financial_needs_1=Decimal("0"), expenditure_limit_1=Decimal("0"), unallocated_task_funds_1=Decimal("0"), contract_amount_1=Decimal("0"), contract_number_1="-",
            financial_needs_2=Decimal("0"), expenditure_limit_2=Decimal("0"), unallocated_task_funds_2=Decimal("0"), contract_amount_2=Decimal("0"), contract_number_2="-",
            financial_needs_3=Decimal("0"), expenditure_limit_3=Decimal("0"), unallocated_task_funds_3=Decimal("0"), contract_amount_3=Decimal("0"), contract_number_3="-",
            
            task_name="History Test Task",
            task_justification="Verifying history tracking",
            expenditure_purpose="Software Testing",
            notes="Version 1: Initial Draft created 30 days ago"
        )
        session.add(row_data_v1)

        # 4. Create History Entry 2: RECENT DATA (e.g., created 7 days ago)
        # Notice: Budget increased to 5000, Contract signed
        date_v2 = datetime.now() - timedelta(days=7)
        row_data_v2 = RowDatas(
            row_id=history_row.id, # Points to SAME row
            last_user_id=user.id,
            last_update=date_v2,   # Newer Date
            
            budget_part="1",
            division_id=division.id,
            chapter_id=chapter.id,
            paragraph_id=paragraph.id,
            expense_group_id=exp_group.id,
            task_budget_full=task_full,
            task_budget_function=task_func,
            funding_source="D3",
            budget_code="WB27.HIST.TEST",
            
            # Values for Version 2 (Changed)
            financial_needs_0=Decimal("5000"), expenditure_limit_0=Decimal("5000"), unallocated_task_funds_0=Decimal("0"), contract_amount_0=Decimal("5000"), contract_number_0="CTR-2024-X",
            financial_needs_1=Decimal("0"), expenditure_limit_1=Decimal("0"), unallocated_task_funds_1=Decimal("0"), contract_amount_1=Decimal("0"), contract_number_1="-",
            financial_needs_2=Decimal("0"), expenditure_limit_2=Decimal("0"), unallocated_task_funds_2=Decimal("0"), contract_amount_2=Decimal("0"), contract_number_2="-",
            financial_needs_3=Decimal("0"), expenditure_limit_3=Decimal("0"), unallocated_task_funds_3=Decimal("0"), contract_amount_3=Decimal("0"), contract_number_3="-",
            
            task_name="History Test Task",
            task_justification="Verifying history tracking",
            expenditure_purpose="Software Testing",
            notes="Version 2: Budget increased and contract signed"
        )
        session.add(row_data_v2)

        # 5. Create History Entry 3: CURRENT DATA (Now)
        # Notice: Budget finalized at 5500
        date_v3 = datetime.now()
        row_data_v3 = RowDatas(
            row_id=history_row.id, # Points to SAME row
            last_user_id=user.id,
            last_update=date_v3,   # Current Date
            
            budget_part="1",
            division_id=division.id,
            chapter_id=chapter.id,
            paragraph_id=paragraph.id,
            expense_group_id=exp_group.id,
            task_budget_full=task_full,
            task_budget_function=task_func,
            funding_source="D3",
            budget_code="WB27.HIST.TEST",
            
            # Values for Version 3 (Final)
            financial_needs_0=Decimal("5500"), expenditure_limit_0=Decimal("5500"), unallocated_task_funds_0=Decimal("500"), contract_amount_0=Decimal("5000"), contract_number_0="CTR-2024-X",
            financial_needs_1=Decimal("0"), expenditure_limit_1=Decimal("0"), unallocated_task_funds_1=Decimal("0"), contract_amount_1=Decimal("0"), contract_number_1="-",
            financial_needs_2=Decimal("0"), expenditure_limit_2=Decimal("0"), unallocated_task_funds_2=Decimal("0"), contract_amount_2=Decimal("0"), contract_number_2="-",
            financial_needs_3=Decimal("0"), expenditure_limit_3=Decimal("0"), unallocated_task_funds_3=Decimal("0"), contract_amount_3=Decimal("0"), contract_number_3="-",
            
            task_name="History Test Task",
            task_justification="Verifying history tracking",
            expenditure_purpose="Software Testing",
            notes="Version 3: Final adjustment made just now"
        )
        session.add(row_data_v3)

        await session.commit()
        print(f"--- History Seed Complete: Created Row ID {history_row.id} with 3 historical versions ---")

    except Exception as e:
        print(f"!!! Error during history seeding: {e}")
        await session.rollback()
        raise e
    


async def seed_like_a_boss(session):
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
            start=datetime.now(),
            end= datetime.now() + timedelta(days=365)
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
            last_update=datetime.now(),
            next_year=False
        )
        session.add(row_1)
        await session.flush() 

        row_data_1 = RowDatas(
            row_id=row_1.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
            last_update=datetime.now(),
            next_year=True 
        )
        session.add(row_2)
        await session.flush() 

        row_data_2 = RowDatas(
            row_id=row_2.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
            last_update=datetime.now(),
            next_year=False
        )
        session.add(row_3)
        await session.flush()

        row_data_3 = RowDatas(
            row_id=row_3.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
            start=datetime.now(),
            end= datetime.now() + timedelta(days=365)
        )
        session.add(dept_table_b)
        await session.flush()

        # 3. Row for dept B
        row_b1 = Rows(
            department_table_id=dept_table_b.id,
            last_update=datetime.now(),
            next_year=False
        )
        session.add(row_b1)
        await session.flush()

        # 4. Row data for dept B
        row_data_b1 = RowDatas(
            row_id=row_b1.id,
            last_user_id=user.id,
            last_update=datetime.now(),
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
   