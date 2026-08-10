"""
metric_source_map — resolve every metric in metric_coverage.csv to a source_id.

Built for the Step-1 metric-selection pass. The registry does not record which clean
file each pipeline writes, and three files are multi-source bundles, so the mapping is
declared explicitly here and VERIFIED (every row must resolve or be explicitly excluded;
resolve_all() prints anything unmatched rather than failing silently).

Rule order: EXCLUDE (non-metric columns) -> BUNDLE prefix rules -> FATF pattern
-> FILE-level default.
"""
import re

# --- Files where the file IS the source ------------------------------------------------
FILE_SOURCE = {
    "vdem_filtered.csv":            "VDEM",
    "wgi_clean.csv":                "WGI",
    "wjp_clean.csv":                "WJP",
    "fh_fiw_clean.csv":             "FH_FIW",
    "fsi_clean.csv":                "FSI",
    "ti_cpi_clean.csv":             "TI_CPI",
    "unodc_clean.csv":              "UNODC_HOMICIDE",
    "ucdp_clean.csv":               "UCDP",
    "powell_thyne_clean.csv":       "POWELL_THYNE",
    "cpj_clean.csv":                "CPJ",
    "civicus_clean.csv":            "CIVICUS",
    "dpi_clean.csv":                "DPI",
    "idea_gsod_clean.csv":          "IDEA_PARTIP",
    "pew_gri_clean.csv":            "PEW_GRI",
    "spi_clean.csv":                "IMF_SPI",
    "odin_clean.csv":               "ODIN",
    "rti_rating_clean.csv":         "RTI_RATING",
    "polfinance_clean.csv":         "TI_POLFINANCE",
    "imf_fiscal_rules_clean.csv":   "IMF_FISCAL_RULES",
    "imapp_clean.csv":              "IMF_IMAPP",
    "areaer_fari_clean.csv":        "IMF_AREAER",
    "areaer_er_clean.csv":          "IMF_AREAER_ERREGIME",
    "chinn_ito_clean.csv":          "CHINN_ITO",
    "wb_brss_clean.csv":            "WB_BRSS",
    "wb_carbon_clean.csv":          "WB_CARBON",
    "climate_laws_clean.csv":       "CLIMATE_LAWS",
    "irena_clean.csv":              "IRENA_CAPACITY",
    "epi_clean.csv":                "YALE_EPI",
    "tfi_clean.csv":                "OECD_TFI",
    "fraser_clean.csv":             "FRASER_REG",     # split by prefix below
    "ascor_clean.csv":              "ASCOR",
    "pefa_clean.csv":               "PEFA",           # LONG format — see PEFA note
}

# --- Bundle files: prefix -> source_id (checked before the file default) ---------------
BUNDLE_PREFIX = {
    "qog_clean.csv": {
        "bci_":            "BCI",
        "ccp_":            "CCP",
        "gpi_":            "GPI",
        "hanson_sigman_":  "HANSON_SIGMAN",
        "kof_":            "KOF_TRADE",
        "nd_gain_":        "ND_GAIN",
        "nelda_":          "NELDA",
        "obs_":            "OBS",
        "pei_":            "PEI",
        "polity5_":        "POLITY5",
        "pts_":            "PTS",
        "romelli_cbi_":    "ROMELLI_CBI",
        "wb_informal_":    "WB_INFORMAL",
    },
    "wdi_clean.csv": {
        "wbl_":            "WB_WBL",
        "wdi_lpi_":        "WB_LPI",
        "wdi_hci_":        "WB_HCI",
        "wdi_":            "WDI",          # catch-all LAST (dict order preserved in 3.7+)
    },
    "fraser_clean.csv": {
        "fraser_legal_":   "FRASER_LEGAL",
        "fraser_regulation": "FRASER_REG",
        "fraser_trade_":   "HERITAGE_TR",  # Fraser Area 4 supersedes Heritage Trade Freedom
    },
}

# --- FATF: bare recommendation / immediate-outcome codes -------------------------------
FATF_PATTERN = re.compile(r"^(R\d+|IO\d+)(_num)?$")

# --- Non-metric columns: identifiers, vintages, provenance flags -----------------------
# Profiled as if they were metrics but carry no governance signal.
EXCLUDE_EXACT = {
    "ifs_code", "country_code_epi", "country_code",
    "pt_version", "areaer_as_of", "areaer_reclassified", "areaer_anchor_currency",
    "framework_version", "indicator_code", "level", "quality_flag", "raw_grade",
    "jurisdiction", "assessment_year", "methodology_round", "report_url",
    "rti_law_year", "wb_carbon_coverage_is_snapshot", "brss_reliable",
    "polfin_n_answered", "wdi_population_total",
}

def resolve(file: str, metric: str):
    """Return (source_id, reason) — source_id is None when the column is excluded."""
    m = str(metric).strip()
    if m in EXCLUDE_EXACT:
        return None, "excluded: identifier/metadata"
    if file == "fatf_clean.csv":
        if FATF_PATTERN.match(m):
            return "FATF", "fatf pattern"
        return None, "excluded: fatf metadata"
    for pref, src in BUNDLE_PREFIX.get(file, {}).items():
        if m.startswith(pref):
            return src, f"bundle prefix {pref!r}"
    if file in FILE_SOURCE:
        return FILE_SOURCE[file], "file default"
    return None, "UNRESOLVED"

def resolve_all(coverage_df, verbose=True):
    """Map every row; print unresolved so gaps are visible, never silent."""
    out = coverage_df.copy()
    res = [resolve(f, m) for f, m in zip(out["file"], out["metric"])]
    out["source_id"] = [r[0] for r in res]
    out["map_reason"] = [r[1] for r in res]
    if verbose:
        unresolved = out[out["map_reason"] == "UNRESOLVED"]
        excluded   = out[out["source_id"].isna() & (out["map_reason"] != "UNRESOLVED")]
        print(f"resolved  : {out['source_id'].notna().sum()} of {len(out)}")
        print(f"excluded  : {len(excluded)} (identifiers/metadata)")
        print(f"UNRESOLVED: {len(unresolved)}")
        if len(unresolved):
            for f, m in zip(unresolved["file"], unresolved["metric"]):
                print(f"    {f:32s} {m}")
    return out