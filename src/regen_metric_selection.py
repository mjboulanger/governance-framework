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

# ---- dictionary cross-check: every scored metric should have a metric_dictionary entry ----
# Reports the gap on every run. Pass --strict to make a nonzero gap a hard failure
# (for use once the backfill is complete).
import sys as _sys
try:
    from metric_dictionary import DICT
except Exception as _e:
    print('\n[dict cross-check] could not import metric_dictionary:', _e)
    DICT = None

if DICT is not None:
    scored_metrics = set(rows[rows.include]['metric'])
    dict_keys = set(DICT)
    missing_from_dict = sorted(scored_metrics - dict_keys)   # scored but undocumented
    orphan_in_dict = sorted(dict_keys - scored_metrics)      # documented but not scored

    print('\n---- metric_dictionary cross-check ----')
    print('scored metrics       :', len(scored_metrics))
    print('dictionary entries   :', len(dict_keys))
    print('documented / to-do   : %d / %d' % (len(scored_metrics) - len(missing_from_dict), len(missing_from_dict)))
    if orphan_in_dict:
        print('ORPHANS (in dict, not scored) -- investigate:')
        for m in orphan_in_dict:
            print('   ', m)
    if missing_from_dict and '--verbose' in _sys.argv:
        print('missing dictionary entries:')
        for m in missing_from_dict:
            print('   ', m)

    if '--strict' in _sys.argv and (missing_from_dict or orphan_in_dict):
        raise SystemExit('[dict cross-check] STRICT: %d missing, %d orphan' %
                         (len(missing_from_dict), len(orphan_in_dict)))