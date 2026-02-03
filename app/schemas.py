from pydantic import BaseModel
from typing import List

class ColumnSchema(BaseModel):
    name: str
    data_type: str

class DatasetCreate(BaseModel):
    fqn: str
    source_type: str
    columns: List[ColumnSchema]

class LineageCreate(BaseModel):
    upstream_fqn: str
    downstream_fqn: str
