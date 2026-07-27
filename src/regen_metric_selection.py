# Regenerates data/processed/metric_selection.csv from src/metric_selection.py
# and prints the concept-health table. Run after any edit to metric_selection.py:
#     python src/regen_metric_selection.py
# Cross-platform: writes LF line endings so the CSV diffs cleanly between Mac and PC.

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from metric_selection import to_rows, D, PENDING

OUT = os.path.join('data', 'processed', 'metric_selection.csv')

rows = pd.DataFrame(to_rows())
try:
    rows.to_csv(OUT, index=False, lineterminator='\n')      # pandas >= 1.5
except TypeError:
    rows.to_csv(OUT, index=False, line_terminator='\n')     # pandas < 1.5

n_scored = int(rows.include.sum())
n_excl = int((~rows.include).sum())
n_dupe = int(rows.duplicated(['metric', 'concept_id']).sum())

print('metrics reviewed : %d' % len(D))
print('rows written     : %d  ->  %s' % (len(rows), OUT))
print('scored / excluded: %d / %d' % (n_scored, n_excl))
print('duplicate metric x concept: %d%s' % (n_dupe, '   <-- INVESTIGATE' if n_dupe else ''))
print('PENDING items    : %d' % len(PENDING))
print()

tab = rows[rows.include].groupby(['concept_id', 'tier']).size().unstack(fill_value=0)
for col in ['P1', 'P2', 'Sp']:
    if col not in tab.columns:
        tab[col] = 0
tab['P1_P2'] = tab.P1 + tab.P2
tab['FLAG'] = tab.P1_P2.map(lambda x: 'THIN' if x < 3 else ('OVER' if x > 11 else ''))
print(tab[['P1', 'P2', 'Sp', 'P1_P2', 'FLAG']].to_string())