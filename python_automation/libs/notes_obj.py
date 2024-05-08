import pandas as pd
import numpy as np
from dataclasses import dataclass

from typing import List, Dict, Optional, Tuple

@dataclass(frozen=True)
class Entry:
    time: float
    event: Optional[str]
    eventstr: Optional[str]
    freq: Optional[float]
    pr: Optional[float]
    pn: Optional[int]
    pd: Optional[float]
    attn: Optional[int]
    iinj: Optional[float]
    pharma: Optional[float]
    input_r: Optional[float]

    @staticmethod
    def fields() -> List[str]:
        return list(Entry.__dataclass_fields__.keys())
    
    @staticmethod
    def mutable_fields() -> List[str]:
        mut_fields: List[str] = Entry.fields()
        mut_fields.remove('time')
        return mut_fields

def read_entries_from_excel(excel_filepath: str) -> List[Entry]:
    try:
        df = pd.read_excel(excel_filepath, header=0, index_col=0)
    except Exception as e:
        print(f"{e}")
        return []
    
    print(df)

    key_map: Dict[str, str] = {field:key for field in Entry.fields() for key in df.keys() if field in key.lower()}
    if len(Entry.fields()) == len(key_map):
        return [Entry(**{field:row[key_map[field]] for field in Entry.fields()}) for _, row in df.iterrows() if not row['IGNORE[bool]'] and not np.isnan(row['IGNORE[bool]'])]
    return []
