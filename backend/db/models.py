from __future__ import annotations
import enum
from datetime import time, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, Integer, SmallInteger, Time, Date, Numeric, Text, ForeignKey, Boolean
from .database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class Authentication(Base):
    __tablename__ = "authentication"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    auth_id: Mapped[int] = mapped_column(ForeignKey("authentication.user_id"), nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_types.id"), nullable=False)

    auth: Mapped["Authentication"] = relationship("Authentication", backref="user", uselist=False)
    department: Mapped["Departments"] = relationship("Departments", backref="users")
    user_type: Mapped["UserTypes"] = relationship("UserTypes", backref="users")

class Departments(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String, nullable=False)

class UserTypes(Base):
    __tablename__ = "user_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String, nullable=False)

class Tables(Base):
    __tablename__ = "tables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    year: Mapped[float] = mapped_column(Numeric(4, 0), nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    isOpen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    budget: Mapped[float] = mapped_column(Numeric(15, 2), nullable=True)

class Statuses(Base):
    __tablename__ = "statuses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String, nullable=False)

class DepartmentTables(Base):
    __tablename__ = "department_tables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)
    start: Mapped[time] = mapped_column(Time, nullable=False)
    end: Mapped[time] = mapped_column(Time, nullable=False)

    table: Mapped["Tables"] = relationship("Tables", backref="department_tables")
    department: Mapped["Departments"] = relationship("Departments", backref="department_tables")
    status: Mapped["Statuses"] = relationship("Statuses", backref="department_tables")

class Rows(Base):
    __tablename__ = "rows"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department_table_id: Mapped[int] = mapped_column(ForeignKey("department_tables.id"), nullable=False)
    last_update: Mapped[time] = mapped_column(Time, nullable=False)
    next_year: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    department_table: Mapped["DepartmentTables"] = relationship("DepartmentTables", backref="rows")

class Divisions(Base):
    __tablename__ = "divisions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String, nullable=False)

class Chapters(Base):
    __tablename__ = "chapters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)

    division: Mapped["Divisions"] = relationship("Divisions", backref="chapters")

class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False) 
    description: Mapped[str] = mapped_column(Text, nullable=True)

class Paragraphs(Base):
    __tablename__ = "paragraphs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id"), nullable=False)
    expense_group_id: Mapped[int] = mapped_column(ForeignKey("expense_groups.id"), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)

    chapter: Mapped["Chapters"] = relationship("Chapters", backref="paragraphs")
    expense_group: Mapped["ExpenseGroups"] = relationship("ExpenseGroups", backref="paragraphs")

class ExpenseGroups(Base):
    __tablename__ = "expense_groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    definition: Mapped[str] = mapped_column(String, nullable=False)

class RowDatas(Base):
    __tablename__ = "row_datas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    row_id: Mapped[int] = mapped_column(ForeignKey("rows.id"), nullable=False)
    last_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    last_update: Mapped[time] = mapped_column(Time, nullable=False)

    budget_part: Mapped[str] = mapped_column(String(2), nullable=False)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"), nullable=False)
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id"), nullable=False)
    paragraph_id: Mapped[int] = mapped_column(ForeignKey("paragraphs.id"), nullable=False)
    funding_source: Mapped[str] = mapped_column(String(1), nullable=True)
    expense_group_id: Mapped[int] = mapped_column(ForeignKey("expense_groups.id"), nullable=False)
    task_budget_full_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    task_budget_function_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    

    program_project_name: Mapped[str] = mapped_column(String, nullable=True)
    organizational_unit_name: Mapped[str] = mapped_column(String, nullable=True)
    plan_wi: Mapped[str] = mapped_column(String, nullable=True)
    fund_distributor: Mapped[str] = mapped_column(String, nullable=True)
    budget_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    task_name: Mapped[str] = mapped_column(String, nullable=True)
    task_justification: Mapped[str] = mapped_column(String, nullable=True)
    expenditure_purpose: Mapped[str] = mapped_column(String, nullable=True)
    financial_needs_0: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    expenditure_limit_0: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unallocated_task_funds_0: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_amount_0: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_number_0: Mapped[str] = mapped_column(String, nullable=False)
    financial_needs_1: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    expenditure_limit_1: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unallocated_task_funds_1: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_amount_1: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_number_1: Mapped[str] = mapped_column(String, nullable=False)
    financial_needs_2: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    expenditure_limit_2: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unallocated_task_funds_2: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_amount_2: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_number_2: Mapped[str] = mapped_column(String, nullable=False)
    financial_needs_3: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    expenditure_limit_3: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unallocated_task_funds_3: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_amount_3: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    contract_number_3: Mapped[str] = mapped_column(String, nullable=False)
    subsidy_agreement_party: Mapped[str] = mapped_column(String, nullable=True)
    legal_basis_for_subsidy: Mapped[str] = mapped_column(String, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    additionals: Mapped[dict] = mapped_column(JSONB, nullable=True)

    row: Mapped["Rows"] = relationship("Rows", backref="row_datas")
    division: Mapped["Divisions"] = relationship("Divisions", backref="row_datas")
    chapter: Mapped["Chapters"] = relationship("Chapters", backref="row_datas")
    paragraph: Mapped["Paragraphs"] = relationship("Paragraphs", backref="row_datas")
    expense_group: Mapped["ExpenseGroups"] = relationship("ExpenseGroups", backref="row_datas")
    task_budget_full: Mapped["Tasks"] = relationship(
            "Tasks", 
            foreign_keys=[task_budget_full_id],
            backref="row_datas_full" 
        )
        
    task_budget_function: Mapped["Tasks"] = relationship(
            "Tasks", 
            foreign_keys=[task_budget_function_id],
            backref="row_datas_function" 
        )