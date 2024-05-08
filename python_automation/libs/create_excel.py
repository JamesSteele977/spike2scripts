import pandas as pd

from typing import List
import os

column_headers: List[str] = [
    "IGNORE[bool]", "TIME[float]", "EVENT[str]", "EVENT_SPEC[str]", "FREQ[float(hz)]", "PR[float(1/s)]", 
    "PN[int]", "PD[float(ms)]", "ATTN[float(db)]", "IINJ[float(nA)]", "PHARMA[str]", "PHARMA_I[float(nA)]", 
    "INPUT_R[float(MOhm)]", "NOTES[str]"
]
df = pd.DataFrame([[0 for j in column_headers]], columns=column_headers)

excel_file_path = './test_excel.xlsx'
if os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):
    os.remove(excel_file_path)
df.to_excel(excel_file_path, index=True)
