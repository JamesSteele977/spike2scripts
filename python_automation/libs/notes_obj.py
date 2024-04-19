import pandas as pd
from dataclasses import dataclass

from typing import List, Dict, Union, Tuple

@dataclass(frozen=True)
class Entry:
    time: float
    event: str
    event_spec: str
    freq: float
    pr: float
    pn: int
    pd: float
    attn: int
    iinj: float
    pharma: float
    input_r: float

def read_entries_from_excel(excel_filepath: str) -> List[Entry]:
    try:
        df = pd.read_excel(excel_filepath, index_col='FILENAME')
    except Exception as e:
        print(str(e))
        return []

    fields: Tuple[str, ...] = tuple(Entry.__dataclass_fields__.keys())
    if not all([field in tuple(df.keys) for field in fields]):
        return []
    
    return [Entry(*{key:row[key.upper()] for key in fields}) for _, row in df.iterrows() if not row['IGNORE']]
