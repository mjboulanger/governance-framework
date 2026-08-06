"""
Normalization transform functions (methodology S5).

This module is the z-family transform ENGINE. It implements the winsorized-z
transform against a fixed-pooled, trailing-20-year baseline, shared by three
method families:
    zscore        : no pre-transform
    log_zscore    : log()   pre-transform (strictly-positive right-skew)
    log1p_zscore  : log1p() pre-transform (zero-inflated counts)

Non-z methods (percentile, occurrence/binary, fixed-anchor pass-through) are
NOT handled here - they are separate and simpler, applied by the orchestration
layer. This module is only the z-spine: the part with the baseline machinery,
and the part the WDI sub-composite build depends on.

Key S5 properties implemented:
  - baseline pooled over the trailing 20-yr window of the metric's OWN panel
    (max non-null year back 19 years; or full history if shorter)
  - params (mean, sd) computed on the TRANSFORMED baseline values
  - the SAME fixed baseline transforms every value (current AND historical)
  - output winsorized to +/-3
  - three baseline-provenance attributes returned alongside
"""
import numpy as np
import pandas as pd

WINDOW_YEARS = 20      # S5 DEFAULT - trailing window length
WINSOR = 3.0           # S5 DEFAULT - winsorization bound (+/- SD)

_PRE = {
    "zscore":       lambda x: x,
    "log_zscore":   lambda x: np.log(x),
    "log1p_zscore": lambda x: np.log1p(x),
}


def normalize_zfamily(df, value_col, method, year_col="year",
                      window_years=WINDOW_YEARS, winsor=WINSOR):
    """Winsorized-z transform of one metric's long panel against its fixed
    trailing-window baseline.

    Parameters
    ----------
    df : DataFrame with at least [year_col, value_col], long panel for ONE metric.
    value_col : name of the raw value column to transform.
    method : one of 'zscore', 'log_zscore', 'log1p_zscore'.

    Returns
    -------
    (out, prov)
      out  : Series aligned to df.index, the winsorized z value (NaN where raw NaN).
      prov : dict with baseline_n_years, baseline_n_obs, baseline_year_span,
             baseline_mean, baseline_sd (the last two on the TRANSFORMED scale).
    """
    if method not in _PRE:
        raise ValueError("normalize_zfamily handles only z-family methods, got %r" % method)
    pre = _PRE[method]

    v = pd.to_numeric(df[value_col], errors="coerce")
    yr = pd.to_numeric(df[year_col], errors="coerce")
    present = v.notna() & yr.notna()

    if present.sum() == 0:
        return pd.Series(np.nan, index=df.index), dict(
            baseline_n_years=0, baseline_n_obs=0, baseline_year_span=None,
            baseline_mean=np.nan, baseline_sd=np.nan)

    # --- resolve the trailing window on the metric's OWN panel ---
    max_yr = int(yr[present].max())
    lo_yr = max_yr - (window_years - 1)
    in_window = present & (yr >= lo_yr) & (yr <= max_yr)

    # --- guard: log() needs strictly positive; log1p needs >= 0 ---
    base_raw = v[in_window]
    if method == "log_zscore" and (base_raw <= 0).any():
        raise ValueError("log_zscore requires strictly positive values; found <=0 in %s" % value_col)
    if method == "log1p_zscore" and (base_raw < 0).any():
        raise ValueError("log1p_zscore requires non-negative values; found <0 in %s" % value_col)

    # --- baseline params on the TRANSFORMED window values ---
    base_t = pre(base_raw.astype(float))
    mu = float(base_t.mean())
    sd = float(base_t.std(ddof=0))   # population SD - pooled reference, not a sample estimate

    win_years = sorted(yr[in_window].dropna().astype(int).unique())
    prov = dict(
        baseline_n_years=len(win_years),
        baseline_n_obs=int(in_window.sum()),
        baseline_year_span=(win_years[0], win_years[-1]) if win_years else None,
        baseline_mean=mu, baseline_sd=sd,
    )

    # --- transform EVERY present value against the fixed baseline ---
    out = pd.Series(np.nan, index=df.index)
    if sd == 0:
        # degenerate: no spread in the window. All present values map to 0 (at the mean).
        out[present] = 0.0
        return out, prov
    all_t = pre(v[present].astype(float))
    z = (all_t - mu) / sd
    out[present] = z.clip(-winsor, winsor)
    return out, prov
