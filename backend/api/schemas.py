from time import time
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime # <-- Imports the specific class
from decimal import Decimal

class DivisionRead(BaseModel):
    id: int
    value: str
    model_config = ConfigDict(from_attributes=True)

class ChapterRead(BaseModel):
    id: int
    value: str
    model_config = ConfigDict(from_attributes=True)

class ParagraphRead(BaseModel):
    id: int
    value: str
    model_config = ConfigDict(from_attributes=True)

class ExpenseGroupRead(BaseModel):
    id: int
    definition: str
    model_config = ConfigDict(from_attributes=True)

class TaskRead(BaseModel):
    id: int
    value: str
    type: str
    description: str
    model_config = ConfigDict(from_attributes=True)

class DepartmentRead(BaseModel):
    id: int
    type: str
    model_config = ConfigDict(from_attributes=True)

class StatusRead(BaseModel):
    id: int
    value: str
    model_config = ConfigDict(from_attributes=True)

class RowDataDTO(BaseModel):
    id: int
    row_id: int
    last_user_id: int
    last_update: datetime

    budget_part: str
    division: DivisionRead = None
    chapter: ChapterRead = None
    paragraph: ParagraphRead = None
    funding_source: Optional[str] = None
    expense_group_id: int
    expense_group: ExpenseGroupRead = None

    task_budget_full: TaskRead = None
    task_budget_function: TaskRead = None
    program_project_name: Optional[str] = None
    organizational_unit_name: Optional[str] = None
    plan_wi: Optional[str] = None
    fund_distributor: Optional[str] = None
    
    budget_code: str
    
    task_name: Optional[str] = None
    task_justification: Optional[str] = None
    expenditure_purpose: Optional[str] = None

    financial_needs_0: Decimal
    expenditure_limit_0: Decimal
    unallocated_task_funds_0: Decimal
    contract_amount_0: Decimal
    contract_number_0: str


    financial_needs_1: Decimal
    expenditure_limit_1: Decimal
    unallocated_task_funds_1: Decimal
    contract_amount_1: Decimal
    contract_number_1: str


    financial_needs_2: Decimal
    expenditure_limit_2: Decimal
    unallocated_task_funds_2: Decimal
    contract_amount_2: Decimal
    contract_number_2: str


    financial_needs_3: Decimal
    expenditure_limit_3: Decimal
    unallocated_task_funds_3: Decimal
    contract_amount_3: Decimal
    contract_number_3: str
    


    subsidy_agreement_party: Optional[str] = None
    legal_basis_for_subsidy: Optional[str] = None
    notes: Optional[str] = None
    
    additionals: Optional[Dict[str, Any]] = None

    

    model_config = ConfigDict(from_attributes=True)

class RowDTO(BaseModel):
    id: int
    last_update: datetime
    next_year: bool
    row_datas: List[RowDataDTO] = []
    model_config = ConfigDict(from_attributes=True)

class DepartmentTableDTO(BaseModel):
    id: int
    start: datetime
    end: datetime
    status: StatusRead
    department: DepartmentRead
    rows: List[RowDTO] = []
    model_config = ConfigDict(from_attributes=True)

class TableFullDTO(BaseModel):
    id: int
    year: float
    version: str
    isOpen: bool
    budget: float
    department_tables: List[DepartmentTableDTO] = []
    model_config = ConfigDict(from_attributes=True)

class ChapterWithParagraphsRead(BaseModel):
    id: int
    value: str
    paragraphs: List['ParagraphRead'] = []
    model_config = ConfigDict(from_attributes=True)

class DivisionWithChaptersRead(BaseModel):
    id: int
    value: str
    chapters: List[ChapterRead] = []
    model_config = ConfigDict(from_attributes=True)

HEADERS = [
    "Część budżetowa",
    "Dział",
    "Rozdział",
    "Paragraf",
    "Źródło finansowania",
    "Grupa wydatków",
    "Budżet zadaniowy (w pełnej szczegółowości)",
    "Budżet zadaniowy (nr funkcji, nr zadania)",
    "Nazwa programu/projektu",

    "Nazwa komórki organizacyjnej",
    "Plan WI",
    "Dysponent środków",
    "Budżet",
    "Nazwa zadania",
    "Szczegółowe uzasadnienie realizacji zadania",
    "Przeznaczenie wydatków wg obszaru działalności: cyberbezpieczeństwo/sztuczna inteligencja/koszty funkcjonowania/inne (wpisać jakie?)",
    
    "Potrzeby finansowe na rok 2026",
    "Limit wydatków na rok 2026",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie\n(kol. 17-kol. 18)",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",
    
    "Potrzeby finansowe na rok 2027",
    "Limit wydatków na rok 2027",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie\n(kol. 22-kol. 23)",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",

    "Potrzeby finansowe na rok 2028",
    "Limit wydatków na rok 2028",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie\n(kol. 27-kol. 28)",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",

    "Potrzeby finansowe na rok 2029",
    "Limit wydatków na rok 2029",
    "Kwota na realizację zadań w 2026 roku, która nie została zabezpieczona w limicie\n(kol. 32-kol. 33)",
    "Kwota zawartej umowy/wniosku o udzielenie zamówienia publicznego",
    "Nr umowy/nr wniosku o udzielenie zamówienia publicznego",
    
    "W przypadku dotacji - z kim zawarta umowa/planowana do zawarcia umowa",    
    "Podstawa prawna udzielenia dotacji",
    "Uwagi",
]
