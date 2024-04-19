import pandas as pd

from typing import List

column_headers: List[str] = [
    "IGNORE", "TIME", "EVENT", "EVENT_SPEC", "FREQ", "PR", 
    "PN", "PD", "ATTN", "IINJ", "PHARMA", "PHARMA_I", "INPUT_R", "NOTES"
]
data_types: List[str] = [
    "bool", "float", "str", "str", "float (hz)", "float (1/s)", "int",
    "float (ms)", "int (db)", "float (nA)", "str", "float (nA)", "float (MOhm)", "str"
]
df = pd.DataFrame([data_types], columns=column_headers)

df.index = ['FILENAME']
df.index.name = 'FILENAME'

excel_file_path = '/mnt/data/headers_excel.xlsx'
df.to_excel(excel_file_path, index=True)
