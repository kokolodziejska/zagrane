import asyncio
from datetime import time, date
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from passlib.hash import argon2

from .database import engine, Base, AsyncSessionLocal
from .models import (
    Authentication, Users, Departments, UserTypes, Tables, 
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

            # FLUSH to generate IDs for Level 1 objects
            await session.flush()

            # ==========================================
            # LEVEL 2: Dependent Objects
            # ==========================================

            # 8. User (Needs Auth, Dept, UserType)
            user = Users(
                auth_id=auth.user_id,
                user_name="admin",
                name="John",
                surname="Doe",
                department_id=dept.id,
                user_type_id=u_type.id
            )
            session.add(user)

            # 9. Chapter (Needs Division)
            chapter = Chapters(
                division_id=div.id,
                value="75023"
            )
            session.add(chapter)

            # 10. Department Table (Needs Table, Dept, Status)
            dept_table = DepartmentTables(
                table_id=table.id,
                department_id=dept.id,
                status_id=stat.id,
                start=time(8, 0),
                end=time(16, 0)
            )
            session.add(dept_table)

            # FLUSH to generate IDs for Level 2 objects
            await session.flush()

            # ==========================================
            # LEVEL 3: Deeply Dependent Objects
            # ==========================================

            # 11. Paragraph (Needs Chapter, ExpenseGroup)
            paragraph = Paragraphs(
                chapter_id=chapter.id,
                expense_group_id=exp_group.id,
                value="400"
            )
            session.add(paragraph)

            # 12. Row (Needs DepartmentTable)
            row = Rows(
                department_table_id=dept_table.id,
                last_update=time(12, 0),
                next_year=False
            )
            session.add(row)

            # FLUSH to generate IDs for Level 3 objects
            await session.flush()

            # ==========================================
            # LEVEL 4: The Data Payload (RowDatas)
            # ==========================================

            # 13. Row Data (Needs EVERYTHING above)
            row_data = RowDatas(
                row_id=row.id,
                last_user_id=user.id,
                last_update=time(12, 30),
                
                # Foreign Keys to Classification
                budget_part="1",
                division_id=div.id,
                chapter_id=chapter.id,
                paragraph_id=paragraph.id,
                expense_group_id=exp_group.id,
                
                # Required Data Fields
                task_budget_full="1.1.1.1.",
                task_budget_function_task="1.1.",
                funding_source="A",
                budget_amount=Decimal("100000.00"),

                
                # Financials - Year 0
                financial_needs_0=Decimal("50000.00"),
                expenditure_limit_0=Decimal("50000.00"),
                unallocated_task_funds_0=Decimal("0.00"),
                contract_amount_0=Decimal("12000.00"),
                contract_number_0="Nie dotyczy",

                
                # Financials - Year 1
                financial_needs_1=Decimal("25000.00"),
                expenditure_limit_1=Decimal("25000.00"),
                unallocated_task_funds_1=Decimal("0.00"),
                contract_amount_1=Decimal("0.00"),
                contract_number_1="Nie dotyczy",


                # Financials - Year 2
                financial_needs_2=Decimal("25000.00"),
                expenditure_limit_2=Decimal("25000.00"),
                unallocated_task_funds_2=Decimal("0.00"),
                contract_amount_2=Decimal("0.00"),
                contract_number_2="Nie dotyczy",


                # Financials - Year 3
                financial_needs_3=Decimal("0.00"),
                expenditure_limit_3=Decimal("0.00"),
                unallocated_task_funds_3=Decimal("0.00"),
                contract_amount_3=Decimal("0.00"),
                contract_number_3="Nie dotyczy",

                
                # Optional text fields
                task_name="Server Maintenance",
                notes="Initial Seed Data"
            )
            session.add(row_data)

            # Final Commit
            await session.commit()
            print("--- Data Seeding Complete: All tables populated ---")

        except Exception as e:
            print(f"!!! Error during seeding: {e}")
            await session.rollback()
            raise e

if __name__ == "__main__":
    asyncio.run(init_db())