from libs.spike2base_class import Spike2SonpyReader
from libs.notes_obj import Entry, read_entries_from_excel

import sys
from typing import List

excel_filepath: str = str()
if len(sys.argv) > 1:
    excel_filepath = sys.argv[1]

while True:
    entries: List[Entry] = read_entries_from_excel(excel_filepath)
    if entries:
        break
    excel_filepath = input('Excel Notes Path: ')

rdr: Spike2SonpyReader = Spike2SonpyReader()


