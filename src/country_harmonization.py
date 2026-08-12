"""
country_harmonization.py — canonical country-key resolution to ISO3.

Single source of truth for joining the ~34 processed source files onto the
country spine. Built from the Step-0 harmonization audit (2026-07-10):
every mapping below was verified against the files' own name columns.

Usage:
    from country_harmonization import add_iso3, TERRITORIES, EXCLUDE_CLOSED
    df = add_iso3(df)              # auto-detects key; adds 'iso3' column (None = drop row)

Design notes:
- Resolution order: explicit code overrides -> ISO3 membership -> name overrides
  -> pycountry exact -> pycountry fuzzy -> parenthetical-strip retry.
- Unresolvable tokens map to None. As of the v3 audit, every None is a verified
  legitimate exclusion (defunct state, quasi-state, or aggregate) — if a NEW token
  appears (source update), it resolves to None and should be caught by the
  coverage checks; add it here explicitly rather than special-casing downstream.
- Powell-Thyne uses COW/GW alpha codes: the divergent live-country codes are in
  CODE_OVERRIDES (verified against the file's country_name column, 2026-07-10).
"""
import pandas as pd

try:
    import pycountry
except ImportError as e:
    raise ImportError("country_harmonization requires pycountry "
                      "(conda env 'governance-framework' has it)") from e

# --------------------------------------------------------------------------- #
# Canonical sets
# --------------------------------------------------------------------------- #
ISO3_SET = {c.alpha_3 for c in pycountry.countries}
ALLOW_EXTRA = {"XKX"}                       # Kosovo — real, non-ISO-standard
VALID = ISO3_SET | ALLOW_EXTRA

EXCLUDE_CLOSED = {"PRK", "ERI", "TKM"}      # [LOCKED] closed-regime spine exclusions

# Non-sovereign territories: kept in data, flagged in spine (is_territory=True)
TERRITORIES = {"HKG","MAC","PRI","BMU","CYM","ABW","CUW","SXM","MAF","TCA","VGB",
               "VIR","GUM","ASM","MNP","NCL","PYF","FRO","GRL","GIB","IMN"}

# Live-country codes that diverge from ISO3 (COW/GW alpha; legacy ISO) — verified
CODE_OVERRIDES = {
    "KOS": "XKX", "OWID_KOS": "XKX", "ROM": "ROU",
    # Powell-Thyne COW/GW alpha (verified vs file's country_name, 2026-07-10):
    "CDI": "CIV", "TAZ": "TZA", "SRI": "LKA", "CAM": "KHM", "BFO": "BFA",
    "RUM": "ROU", "BOS": "BIH", "DRC": "COD", "DRV": "VNM", "GFR": "DEU",
    "AAB": "ATG",
}

# Deliberate drops: defunct states, quasi-states, aggregates (verified legitimate)
DROP_TOKENS = {
    "_EA", "CHI", "ANT", "DDR", "GDR", "CSK", "SUN", "YUG", "SCG", "YMD", "YPR",
    "ZZB", "SML", "PSG", "SOT", "HIC", "LIC", "LMC", "UMC",
    # WDI regional/income aggregates:
    "AFE","AFW","ARB","CEB","CSS","EAP","EAR","EAS","ECA","ECS","EMU","EUU",
    "FCS","HPC","IBD","IBT","IDA","IDB","IDX","INX","LAC","LCN","LDC","LIE_X",
    "LMY","LTE","MEA","MIC","MNA","NAC","OED","OSS","PRE","PSS","PST","SAS",
    "SSA","SSF","SST","TEA","TEC","TLA","TMN","TSA","TSS","WLD",
}
DROP_PREFIXES = ("OWID_", "UN_")

NAME_OVERRIDES = {
    "democratic republic of congo": "COD", "democratic republic of the congo": "COD",
    "dr congo": "COD", "congo, dem. rep.": "COD", "congo kinshasa": "COD", "drc": "COD",
    "congo (drc)": "COD", "congo (kinshasa)": "COD", "congo democratic republic": "COD",
    "republic of congo": "COG", "congo, rep.": "COG", "congo brazzaville": "COG",
    "congo (brazzaville)": "COG", "congo republic": "COG", "congo": "COG",
    "ivory coast": "CIV", "cote d'ivoire": "CIV", "c\u00f4te d'ivoire": "CIV",
    "south korea": "KOR", "korea, rep.": "KOR", "republic of korea": "KOR",
    "korea south": "KOR",
    "north korea": "PRK", "korea, dem. people's rep.": "PRK", "korea north": "PRK",
    "russia": "RUS", "russian federation": "RUS",
    "syria": "SYR", "syrian arab republic": "SYR",
    "iran": "IRN", "iran, islamic rep.": "IRN",
    "venezuela": "VEN", "venezuela, rb": "VEN",
    "bolivia": "BOL", "tanzania": "TZA", "vietnam": "VNM", "viet nam": "VNM",
    "laos": "LAO", "lao pdr": "LAO", "lao people's democratic republic": "LAO",
    "moldova": "MDA", "brunei": "BRN", "brunei darussalam": "BRN",
    "czech republic": "CZE", "czechia": "CZE", "czech rep.": "CZE",
    "slovakia": "SVK", "slovak republic": "SVK",
    "macedonia": "MKD", "north macedonia": "MKD", "fyrom": "MKD",
    "kosovo": "XKX",
    "palestine": "PSE", "west bank and gaza": "PSE", "state of palestine": "PSE",
    "palestinian territories": "PSE", "occupied palestinian territories": "PSE",
    "taiwan": "TWN", "taiwan, china": "TWN",
    "hong kong": "HKG", "hong kong sar, china": "HKG",
    "macau": "MAC", "macao sar, china": "MAC",
    "micronesia": "FSM", "micronesia, fed. sts.": "FSM",
    "gambia": "GMB", "the gambia": "GMB", "gambia, the": "GMB",
    "bahamas": "BHS", "the bahamas": "BHS", "bahamas, the": "BHS",
    "united states": "USA", "united states of america": "USA", "usa": "USA",
    "united kingdom": "GBR", "uk": "GBR", "great britain": "GBR",
    "turkey": "TUR", "turkiye": "TUR", "t\u00fcrkiye": "TUR",
    "swaziland": "SWZ", "eswatini": "SWZ",
    "cape verde": "CPV", "cabo verde": "CPV", "c. verde is.": "CPV",
    "burma": "MMR", "myanmar": "MMR", "myanmar (burma)": "MMR",
    "east timor": "TLS", "timor-leste": "TLS", "timor leste": "TLS",
    "egypt": "EGY", "egypt, arab rep.": "EGY", "yemen": "YEM", "yemen, rep.": "YEM",
    "kyrgyzstan": "KGZ", "kyrgyz republic": "KGZ",
    "st. lucia": "LCA", "saint lucia": "LCA",
    "st. vincent and the grenadines": "VCT", "saint vincent and the grenadines": "VCT",
    "st vincent and the grenadines": "VCT",
    "st. kitts and nevis": "KNA", "saint kitts and nevis": "KNA",
    "st kitts and nevis": "KNA",
    "trinidad": "TTO", "trinidad and tobago": "TTO", "trinidad & tobago": "TTO",
    "trinidad-tobago": "TTO",
    "central african republic": "CAF", "cent. af. rep.": "CAF",
    "south sudan": "SSD", "sudan": "SDN",
    "guinea-bissau": "GNB", "guinea bissau": "GNB",
    "papua new guinea": "PNG", "p. n. guinea": "PNG",
    "sao tome and principe": "STP", "s\u00e3o tom\u00e9 and pr\u00edncipe": "STP",
    # DPI abbreviations (verified 2026-07-10):
    "prc": "CHN", "s. africa": "ZAF", "dom. rep.": "DOM", "eq. guinea": "GNQ",
    "comoro is.": "COM", "solomon is.": "SLB", "frg/germany": "DEU", "uae": "ARE",
    "bosnia-herz": "BIH", "bosnia & herzegovina": "BIH", "bosnia-herzegovina": "BIH",
    "antigua & barbuda": "ATG",
    "israel and west bank": "ISR",
}

# Per-file key hints (from the Step-0 audit); everything else auto-detects
KEY_HINTS = {
    "vdem_filtered.csv": "country_text_id",
    "cpj_clean.csv": "iso3", "fatf_clean.csv": "iso3", "tfi_clean.csv": "iso3",
    "ucdp_clean.csv": "country_id",
}
NAME_KEYED = {"civicus_clean.csv", "dpi_clean.csv", "fh_fiw_clean.csv",
              "fsi_clean.csv", "pew_gri_clean.csv"}

# --------------------------------------------------------------------------- #
# Resolvers
# --------------------------------------------------------------------------- #
def resolve_iso3_code(token):
    """3-letter (or override-listed) code -> ISO3 or None (drop)."""
    if token is None or (isinstance(token, float) and pd.isna(token)):
        return None
    t = str(token).strip().upper()
    if not t:
        return None
    if t in CODE_OVERRIDES:
        return CODE_OVERRIDES[t]
    if t in DROP_TOKENS or any(t.startswith(p) for p in DROP_PREFIXES):
        return None
    return t if t in VALID else None


DROP_NAMES = {"zanzibar", "somaliland", "south yemen",
              "german democratic republic", "palestine/gaza",
              "africa", "africa (un)"}


def resolve_iso3_name(name):
    """Country name -> ISO3 or None. Overrides -> exact -> fuzzy -> strip-().-retry."""
    if not isinstance(name, str) or not name.strip():
        return None
    if name.strip().lower() in DROP_NAMES:
        return None
    k = name.strip().lower()
    if k in NAME_OVERRIDES:
        return NAME_OVERRIDES[k]
    try:
        return pycountry.countries.lookup(name.strip()).alpha_3
    except LookupError:
        pass
    try:
        hits = pycountry.countries.search_fuzzy(name.strip())
        if hits:
            return hits[0].alpha_3
    except LookupError:
        pass
    if "(" in name:  # "Russia (Soviet Union)" pattern
        base = name.split("(")[0].strip()
        if base and base.lower() != k:
            return resolve_iso3_name(base)
    return None


def detect_country_key(df, filename_hint=None):
    """Best country-key column for a processed frame."""
    if filename_hint and filename_hint in KEY_HINTS \
            and KEY_HINTS[filename_hint] in df.columns:
        return KEY_HINTS[filename_hint]
    for cand in ("country_code", "iso3", "country_text_id", "country_name",
                 "country_id", "country"):
        if cand in df.columns:
            return cand
    return None


def add_iso3(df, key=None, filename_hint=None, out_col="iso3"):
    """
    Return a copy of df with an ISO3 column added (None where unresolvable —
    caller drops or inspects). Code-first, name-fallback resolution.
    """
    df = df.copy()
    key = key or detect_country_key(df, filename_hint)
    if key is None:
        raise ValueError("No country key column detected; pass key= explicitly.")
    toks = df[key].astype(str).str.strip()

    name_col = next((c for c in ("country_name", "country", "location")
                     if c in df.columns and c != key), None)

    if (filename_hint in NAME_KEYED) or key in ("country_name", "country"):
        iso = toks.map(resolve_iso3_name)
    elif key == "country_id" or toks.str.fullmatch(r"\d+(\.\d+)?").fillna(False).mean() > 0.8:
        if name_col is None:
            raise ValueError(f"Numeric-id key '{key}' with no name column — needs explicit map.")
        iso = df[name_col].map(resolve_iso3_name)
    else:
        iso = toks.map(resolve_iso3_code)
        if name_col is not None:               # name fallback for code misses
            fb = df.loc[iso.isna(), name_col].map(resolve_iso3_name)
            iso.loc[iso.isna()] = fb

    df[out_col] = iso
    return df
