"""concept_sources - declares which sources feed which concept, for the Step-1 pass.

Transcribed 2026-07-22 from the Build-Status audit in framework_decisions.md, with three
corrections where the audit is stale: C10 state-control un-deferred (v2clstown, 2026-07-21),
C12 ND-GAIN dropped + ASCOR added (2026-07-22). Only status=='built' rows generate candidate
metrics; outstanding/closed are recorded so decisions are not re-litigated.
"""

CATS = {
    1: "Political foundations", 2: "State capacity",
    3: "Economic and fiscal governance", 4: "Rule of law", 5: "Accountability",
}

CONCEPTS = {
 1:  dict(name="Political settlement", cats=[1], built=["VDEM","FSI","DPI"], outstanding=[], closed=[]),
 2:  dict(name="Political stability and regime durability", cats=[1], built=["WGI","VDEM","POWELL_THYNE","UCDP","GPI","WJP"], outstanding=["ACLED"], closed=[]),
 3:  dict(name="Statistical and informational infrastructure", cats=[2,5], built=["IMF_SPI","ODIN"], outstanding=[], closed=["IMF_SPI_SDDS"]),
 4:  dict(name="Government effectiveness and administrative quality", cats=[2], built=["WGI","VDEM"], outstanding=[], closed=[]),
 5:  dict(name="Service delivery and provision of public goods", cats=[2], built=["WDI","WB_HCI","FSI"], outstanding=[], closed=["WHO_GHO","UNESCO_UIS","UNDP_HDI"]),
 6:  dict(name="Regulatory quality", cats=[3,2], built=["WGI","WJP","FRASER_REG"], outstanding=[], closed=[]),
 7:  dict(name="Public financial management", cats=[3], built=["PEFA","OBS"], outstanding=[], closed=[]),
 8:  dict(name="Macroeconomic and financial policy framework", cats=[3], built=["ROMELLI_CBI","IMF_FISCAL_RULES","IMF_AREAER","CHINN_ITO","IMF_IMAPP","IMF_AREAER_ERREGIME"], outstanding=[], closed=["DINCER_CB","REINHART_ROGOFF"]),
 9:  dict(name="Financial sector regulatory and supervisory quality", cats=[3], built=["FATF","WB_BRSS"], outstanding=["FSAP","BASEL_AML"], closed=[]),
 10: dict(name="State control over the economy", cats=[3], built=["VDEM"], outstanding=[], closed=[]),
 11: dict(name="Trade governance", cats=[3], built=["WB_LPI","OECD_TFI","WDI","HERITAGE_TR"], outstanding=[], closed=["WTO_TFA","KOF_TRADE","UNCTAD_NTM"]),
 12: dict(name="Environmental and climate governance", cats=[3], built=["YALE_EPI","CLIMATE_LAWS","IRENA_CAPACITY","WB_CARBON","ASCOR"], outstanding=[], closed=["ND_GAIN","IRENA_POLICY"]),
 13: dict(name="State capacity (structural core)", cats=[2], built=["VDEM","FSI","WB_INFORMAL","HANSON_SIGMAN"], outstanding=["ILO_SOCIAL"], closed=[]),
 14: dict(name="Legal quality and predictability", cats=[4], built=["VDEM","WJP","CCP"], outstanding=[], closed=[]),
 15: dict(name="Judicial independence and quality", cats=[4,5], built=["VDEM","WJP"], outstanding=[], closed=["LINZER_STATON"]),
 16: dict(name="Personal security and order", cats=[4], built=["UNODC_HOMICIDE","VDEM","PTS","WJP","GPI"], outstanding=[], closed=[]),
 17: dict(name="Property rights and contract enforcement", cats=[4], built=["VDEM","WJP","FRASER_LEGAL","WDI"], outstanding=[], closed=["HERITAGE_PR"]),
 18: dict(name="Control of corruption", cats=[4], built=["VDEM","TI_CPI","WJP","BCI"], outstanding=[], closed=[]),
 19: dict(name="Legislative and constitutional checks", cats=[5,4], built=["VDEM","CCP","POLITY5"], outstanding=[], closed=["IPU_PARLINE"]),
 20: dict(name="Electoral process and competition", cats=[5], built=["VDEM","FH_FIW","PEI","NELDA"], outstanding=[], closed=["IDEA_EMB"]),
 21: dict(name="Political participation beyond voting", cats=[5], built=["VDEM","CIVICUS","IDEA_PARTIP"], outstanding=[], closed=[]),
 22: dict(name="Civil liberties", cats=[5], built=["FH_FIW","VDEM","PEW_GRI","PTS","WB_WBL"], outstanding=[], closed=[]),
 23: dict(name="Media freedom and pluralism", cats=[5], built=["VDEM","FH_FIW","RTI_RATING","CPJ"], outstanding=[], closed=["RSF_WPFI"]),
 24: dict(name="Civil society space and vitality", cats=[5], built=["VDEM","CIVICUS","FH_FIW"], outstanding=[], closed=["ICNL"]),
 25: dict(name="Government transparency and openness", cats=[5], built=["VDEM","WJP","RTI_RATING","OBS","TI_POLFINANCE"], outstanding=[], closed=["GLOBAL_DATA_BAROMETER"]),
}

def to_rows():
    rows = []
    for cid, c in CONCEPTS.items():
        for status in ("built", "outstanding", "closed"):
            for src in c[status]:
                rows.append(dict(concept_id=cid, concept_name=c["name"],
                                 category=CATS[c["cats"][0]],
                                 multi_placed=len(c["cats"]) > 1,
                                 category_2=CATS[c["cats"][1]] if len(c["cats"]) > 1 else "",
                                 source_id=src, status=status))
    return rows

if __name__ == "__main__":
    # Regenerate the review CSV data/processed/concept_sources.csv from this
    # source-of-truth. The scoring pipeline reads to_rows() directly (no CSV
    # dependency); this CSV is a gitignored convenience artifact for eyeballing
    # / spreadsheet review only. Run: python src/concept_sources.py
    import os, csv
    rows = to_rows()
    out = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "concept_sources.csv")
    out = os.path.normpath(out)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", out, "(%d rows)" % len(rows))
