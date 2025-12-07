from datetime import datetime
from typing import Dict, Any, List, Optional
import json

class RowDataMapper:

    VALUE_FIELD_MAP = {
        "budget_part": 0,
        "division_value": 1,          
        "chapter_value": 2,            
        "paragraph_value": 3,          
        "funding_source": 4,
        "expense_group_value": 5,      
        "task_budget_full_value": 6,   
        "task_budget_function_value": 7, 
        "program_project_name": 8,
        "organizational_unit_name": 9,
        "plan_wi": 10,
        "fund_distributor": 11,
        "budget_code": 12,
        "task_name": 13,
        "task_justification": 14,
        "expenditure_purpose": 15,
        "financial_needs_0": 16,
        "expenditure_limit_0": 17,
        "unallocated_task_funds_0": 18,
        "contract_amount_0": 19,
        "contract_number_0": 20,
        "financial_needs_1": 21,
        "expenditure_limit_1": 22,
        "unallocated_task_funds_1": 23,
        "contract_amount_1": 24,
        "contract_number_1": 25,
        "financial_needs_2": 26,
        "expenditure_limit_2": 27,
        "unallocated_task_funds_2": 28,
        "contract_amount_2": 29,
        "contract_number_2": 30,
        "financial_needs_3": 31,
        "expenditure_limit_3": 32,
        "unallocated_task_funds_3": 33,
        "contract_amount_3": 34,
        "contract_number_3": 35,
        "subsidy_agreement_party": 36,
        "legal_basis_for_subsidy": 37,
        "notes": 38,
        "additionals": 39,
    }

    @staticmethod
    def _to_float(value: str) -> float:
        if not value or value.strip().lower() in ["", "nie dotyczy", "-", "draft"]:
            return 0.0
        try:
            return float(value)
        except ValueError:
            return 0.0 

    @staticmethod
    def _to_jsonb(value: str) -> Optional[Dict]:
        if not value:
            return None 
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}
    
    @classmethod
    def map_row_data(cls, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        mapped_data = {}
        values = raw_data.get("values", [])

        mapped_data["row_id"] = raw_data.get("rowId")
        mapped_data["last_user_id"] = raw_data.get("lastUserId")
        
        try:
            mapped_data["last_update"] = datetime.fromisoformat(raw_data["lastUpdate"].replace("Z", "+00:00"))
        except (ValueError, KeyError):
            mapped_data["last_update"] = datetime.utcnow() 

        for field_name, index in cls.VALUE_FIELD_MAP.items():
            raw_value = values[index] if index < len(values) else None
            
            if field_name.startswith(("financial_needs", "expenditure_limit", "unallocated_task_funds", "contract_amount")):
                mapped_data[field_name] = cls._to_float(raw_value)
            elif field_name == "additionals":
                mapped_data[field_name] = cls._to_jsonb(raw_value)
            elif raw_value is not None:
                mapped_data[field_name] = str(raw_value).strip()
            else:
                mapped_data[field_name] = None

        return mapped_data