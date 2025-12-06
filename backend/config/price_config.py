from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import date

class PriceMeta(BaseModel):
    model_config = ConfigDict(extra='forbid')
    validFrom: date
    validTo: date
    currency: str  
    unit: int

class TableConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: int
    title: str
    subtitle: str
    headers: List[str] = Field(min_length=1)
    descriptions: List[str] = []

class DescriptionBlock(BaseModel):
    model_config = ConfigDict(extra='forbid')
    header: str
    text: List[str] = []

class PriceConfigSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: int
    title: str
    meta: PriceMeta
    tables: List[TableConfig] = Field(min_length=1)
    descriptions: List[DescriptionBlock] = []
