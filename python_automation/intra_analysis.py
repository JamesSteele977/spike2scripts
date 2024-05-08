import numpy as np

from libs.spike2base_class import Spike2SonpyReader
from libs.notes_obj import Entry, read_entries_from_excel

import sys, os
from typing import List

excel_filepath: str = str()
spike2_filepath: str = str()
if len(sys.argv) > 2:
    excel_filepath = sys.argv[1]
    spike2_filepath = sys.argv[2]

while True:
    entries: List[Entry] = read_entries_from_excel(excel_filepath)
    if entries and os.path.exists(spike2_filepath) and os.path.isfile(spike2_filepath):
        break
    excel_filepath = input('Excel Notes Path: ')
    spike2_filepath = input('Spike2 Path: ')

rdr: Spike2SonpyReader = Spike2SonpyReader(spike2_filepath)

# Process loop:

print(len(entries))

ref: Entry = entries[0]
for entry in enumerate(entries[1:]):
    for field in Entry.mutable_fields():
        prior = entry.__dict__[field]
        if prior is None or np.isnan(prior):
            entry.__dict__[field] = ref.__dict__[field]
        else:
            ref.__dict__[field] = prior

print('\t'.join([key for key in Entry.fields()]))
for entry in entries:
    print('\t'.join([str(val) for val in entry.__dict__.values()]))




