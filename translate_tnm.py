#!/usr/bin/env python3
"""Translate TNM tool index.html from Italian to English → index-en.html"""

import re, sys

import os
SRC = os.environ.get('TNM_SRC', 'index.html')
DST = os.environ.get('TNM_DST', 'index-en.html')

with open(SRC, encoding='utf-8') as f:
    txt = f.read()

R = []

# ════════════════════════════════════════════════════════════════════════════
# 1. HTML HEAD & LANG
# ════════════════════════════════════════════════════════════════════════════
R += [
  ('<html lang="it">', '<html lang="en">'),
  ('TNM 9ª Ed. v1.0 — Anatomia Patologica · 29 sedi',
   'TNM 9th Ed. v1.0 — Surgical Pathology · 29 sites'),
]

# ════════════════════════════════════════════════════════════════════════════
# 2. SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
R += [
  ('<h1>TNM 9ª Ed.</h1>', '<h1>TNM 9th Ed.</h1>'),
  ('<small>UICC 2025 · 29 sedi</small>', '<small>UICC 2025 · 29 sites</small>'),
  ('placeholder="🔍  Cerca sede…"', 'placeholder="🔍  Search site…"'),
]

# ════════════════════════════════════════════════════════════════════════════
# 3. TOPBAR
# ════════════════════════════════════════════════════════════════════════════
R += [
  ('>📋 Definizioni<', '>📋 Definitions<'),
  ('>🎯 Stadiazione<', '>🎯 Staging<'),
  ('>📄 Referto<', '>📄 Report<'),
  ('>🆕 Nuovo caso<', '>🆕 New case<'),
  ('<h2>TNM 9ª Edizione</h2>', '<h2>TNM 9th Edition</h2>'),
  ('<p>Seleziona una sede tumorale dal pannello di sinistra</p>',
   '<p>Select a tumor site from the left panel</p>'),
  ('>Seleziona una sede<', '>Select a site<'),
]

# ════════════════════════════════════════════════════════════════════════════
# 4. STAGING FORM
# ════════════════════════════════════════════════════════════════════════════
R += [
  ('<label>LN esaminati</label>', '<label>LN examined</label>'),
  ('<label>LN positivi → auto-calcola N ↓</label>',
   '<label>LN positive → auto-calculate N ↓</label>'),
  ('placeholder="es. 24"', 'placeholder="e.g. 24"'),
  ('placeholder="es. 3"',  'placeholder="e.g. 3"'),
  ('<label>Dim. LN maggiore (mm) → auto-N ↓</label>',
   '<label>Largest LN (mm) → auto-N ↓</label>'),
  ('placeholder="es. 18"', 'placeholder="e.g. 18"'),
  ('<label>ENE (gh. salivari)</label>', '<label>ENE (salivary glands)</label>'),
  ('<option value="neg">ENE− (assente)</option>', '<option value="neg">ENE− (absent)</option>'),
  ('<option value="pos">ENE+ (presente)</option>', '<option value="pos">ENE+ (present)</option>'),
  ('<label>T — Tumore primitivo</label>', '<label>T — Primary tumor</label>'),
  ('<label>N — Linfonodi regionali</label>', '<label>N — Regional lymph nodes</label>'),
  ('<label>M — Metastasi a distanza</label>', '<label>M — Distant metastasis</label>'),
  ('>Calcola Stadio<', '>Calculate Stage<'),
  ('"Stadio (TNM 9ª Ed.)"', '"Stage (TNM 9th Ed.)"'),
  # staging table header
  ('<th>Stadio</th>', '<th>Stage</th>'),
  ('<th>Note</th>', '<th>Notes</th>'),
]

# ════════════════════════════════════════════════════════════════════════════
# 5. REFERTO FORM
# ════════════════════════════════════════════════════════════════════════════
R += [
  ('Variante/Istotipo:</label>', 'Variant/Histotype:</label>'),
  # prefix label
  ('<label>Prefisso TNM <span style="color:var(--accent2);font-weight:700">*</span></label>',
   '<label>TNM Prefix <span style="color:var(--accent2);font-weight:700">*</span></label>'),
  # M source label
  ('<label>Fonte M <span style="color:var(--muted);font-weight:400;font-size:10px">(M spesso non è patologico)</span></label>',
   '<label>M source <span style="color:var(--muted);font-weight:400;font-size:10px">(M is often not pathological)</span></label>'),
  # prefix options
  ('<option value="p">p — patologico (post-chirurgia)</option>',
   '<option value="p">p — pathological (post-surgery)</option>'),
  ('<option value="yp">yp — post-neoadiuvante</option>',
   '<option value="yp">yp — post-neoadjuvant</option>'),
  ('<option value="r">r — recidiva</option>',
   '<option value="r">r — recurrence</option>'),
  ('<option value="c">c — clinico (pre-chirurgia)</option>',
   '<option value="c">c — clinical (pre-surgery)</option>'),
  # M source options
  ('<option value="cM">cM — clinico/radiologico (default)</option>',
   '<option value="cM">cM — clinical/radiological (default)</option>'),
  ('<option value="pM">pM — patologico (biopsia metastasi)</option>',
   '<option value="pM">pM — pathological (metastasis biopsy)</option>'),
  ('<option value="ycM">ycM — post-trattamento, clinico/radiologico</option>',
   '<option value="ycM">ycM — post-treatment, clinical/radiological</option>'),
  ('<option value="ypM">ypM — post-trattamento, patologico</option>',
   '<option value="ypM">ypM — post-treatment, pathological</option>'),
  ('<option value="MX">MX — non documentato</option>',
   '<option value="MX">MX — not documented</option>'),
  # LN fields
  ('<label>Linfonodi esaminati</label>', '<label>Lymph nodes examined</label>'),
  ('<label>Linfonodi positivi</label>',  '<label>Positive lymph nodes</label>'),
  ('<label>Note aggiuntive (opzionale)</label>', '<label>Additional notes (optional)</label>'),
  ('placeholder="es. invasione linfovascolare, margini, regressione..."',
   'placeholder="e.g. lymphovascular invasion, margins, regression..."'),
  # prognostic factors header
  ('Fattori prognostici non-TNM <span style="font-weight:400;text-transform:none">(opzionale — solo i campi valorizzati compariranno nel referto)</span>',
   'Non-TNM prognostic factors <span style="font-weight:400;text-transform:none">(optional — only completed fields will appear in the report)</span>'),
  # LVI
  ('<label>LVI — Invasione linfovascolare</label>', '<label>LVI — Lymphovascular invasion</label>'),
  ('<option value="">— non indicato —</option>', '<option value="">— not specified —</option>'),
  ('<option value="LVI presente">Presente</option>',
   '<option value="LVI present">Present</option>'),
  ('<option value="LVI non identificata nel campione">Non identificata nel campione</option>',
   '<option value="LVI not identified in the sample">Not identified in the sample</option>'),
  ('<option value="LVI non valutabile">Non valutabile</option>',
   '<option value="LVI not assessable">Not assessable</option>'),
  # PNI
  ('<label>PNI — Invasione perineurale</label>', '<label>PNI — Perineural invasion</label>'),
  ('<option value="PNI presente">Presente</option>',
   '<option value="PNI present">Present</option>'),
  ('<option value="PNI non identificata nel campione">Non identificata nel campione</option>',
   '<option value="PNI not identified in the sample">Not identified in the sample</option>'),
  ('<option value="PNI non valutabile">Non valutabile</option>',
   '<option value="PNI not assessable">Not assessable</option>'),
  # Budding
  ('<label>Budding tumorale <span style="font-size:10px;color:var(--muted)">(ITBCC 2016)</span></label>',
   '<label>Tumor budding <span style="font-size:10px;color:var(--muted)">(ITBCC 2016)</span></label>'),
  ('<option value="Budding Bd1 (basso, 0–4 buds/0.785mm²)">Bd1 — basso</option>',
   '<option value="Budding Bd1 (low, 0–4 buds/0.785mm²)">Bd1 — low</option>'),
  ('<option value="Budding Bd2 (intermedio, 5–9 buds/0.785mm²)">Bd2 — intermedio</option>',
   '<option value="Budding Bd2 (intermediate, 5–9 buds/0.785mm²)">Bd2 — intermediate</option>'),
  ('<option value="Budding Bd3 (alto, ≥10 buds/0.785mm²)">Bd3 — alto</option>',
   '<option value="Budding Bd3 (high, ≥10 buds/0.785mm²)">Bd3 — high</option>'),
  # Margins
  ('<label>Margini di resezione</label>', '<label>Resection margins</label>'),
  ('<option value="R0 (margini liberi)">R0 — liberi</option>',
   '<option value="R0 (free margins)">R0 — free</option>'),
  ('<option value="R1 (margine microscopicamente coinvolto)">R1 — microscopico</option>',
   '<option value="R1 (microscopically involved margin)">R1 — microscopic</option>'),
  ('<option value="R2 (margine macroscopicamente coinvolto)">R2 — macroscopico</option>',
   '<option value="R2 (macroscopically involved margin)">R2 — macroscopic</option>'),
  ('<option value="RX (non valutabile)">RX — non valutabile</option>',
   '<option value="RX (not assessable)">RX — not assessable</option>'),
  # Regression
  ('<label>Regressione post-neoadiuvante</label>', '<label>Post-neoadjuvant regression</label>'),
  ('<option value="Ryan 0 — risposta completa (no tumore residuo)">Ryan 0 — completa</option>',
   '<option value="Ryan 0 — complete response (no residual tumor)">Ryan 0 — complete</option>'),
  ('<option value="Ryan 1 — risposta quasi completa (raro tumore residuo)">Ryan 1 — quasi completa</option>',
   '<option value="Ryan 1 — near-complete response (rare residual tumor)">Ryan 1 — near-complete</option>'),
  ('<option value="Ryan 2 — risposta parziale (tumore residuo con fibrosi)">Ryan 2 — parziale</option>',
   '<option value="Ryan 2 — partial response (residual tumor with fibrosis)">Ryan 2 — partial</option>'),
  ('<option value="Ryan 3 — risposta minima o assente (tumore esteso residuo)">Ryan 3 — minima/assente</option>',
   '<option value="Ryan 3 — minimal or absent response (extensive residual tumor)">Ryan 3 — minimal/absent</option>'),
  # Perforation
  ('<label>Perforazione</label>', '<label>Perforation</label>'),
  ('<option value="Perforazione assente">Assente</option>',
   '<option value="Perforation absent">Absent</option>'),
  ('<option value="Perforazione presente">Presente</option>',
   '<option value="Perforation present">Present</option>'),
  # Buttons
  ('>Genera Referto<', '>Generate Report<'),
]

# ════════════════════════════════════════════════════════════════════════════
# 6. DISCLAIMER
# ════════════════════════════════════════════════════════════════════════════
R += [
  ('⚠️ Uso esclusivo anatomia patologica · UICC TNM 9ª ed. 2025 / AJCC Cancer Staging Manual Version 9 · Non sostituisce la valutazione clinico-patologica · Verificare fonte primaria per casi borderline · v1.0',
   '⚠️ For use in surgical pathology only · UICC TNM 9th ed. 2025 / AJCC Cancer Staging Manual Version 9 · Does not replace clinicopathological assessment · Always verify borderline cases against the primary source · v1.0'),
]

# ════════════════════════════════════════════════════════════════════════════
# 7. JS: TOOL_META & CATS
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("dataset:'UICC TNM Classification of Malignant Tumours, 9ª ed. (2025)'",
   "dataset:'UICC TNM Classification of Malignant Tumours, 9th ed. (2025)'"),
  ("validazione_automatica:'153/153 casi-test PASS'",
   "validazione_automatica:'153/153 test cases PASS'"),
  ("validazione_manuale:'29/29 sedi auditate — 27 validate, 1 parziale (Mammella), 1 con riserva (Canale anale)'",
   "validazione_manuale:'29/29 sites audited — 27 validated, 1 partial (Breast), 1 with caveat (Anal canal)'"),
  ("responsabile:'F.M.D. Bianchi, SC Anatomia Patologica, ASST FBF-Sacco Milano'",
   "responsabile:'F.M.D. Bianchi, Division of Pathology, ASST FBF-Sacco Milan'"),
  ("gi:{label:'Apparato digerente',order:0}",   "gi:{label:'Gastrointestinal',order:0}"),
  ("gi_net:{label:'NET Gastrointestinali',order:1}", "gi_net:{label:'GI Neuroendocrine Tumors',order:1}"),
  ("hn:{label:'Testa e Collo',order:2}",         "hn:{label:'Head and Neck',order:2}"),
  ("breast:{label:'Mammella',order:3}",          "breast:{label:'Breast',order:3}"),
  ("uro:{label:'Urologico',order:4}",            "uro:{label:'Urological',order:4}"),
  ("skin:{label:'Cute / Melanoma',order:5}",     "skin:{label:'Skin / Melanoma',order:5}"),
]

# ════════════════════════════════════════════════════════════════════════════
# 8. JS: COMPLETENESS_BADGE & renderLookup
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("complete:{cls:'badge-complete',icon:'✓',label:'Completo'}",
   "complete:{cls:'badge-complete',icon:'✓',label:'Complete'}"),
  ("partial: {cls:'badge-partial', icon:'◑',label:'Parziale — alcune funzioni non implementate'}",
   "partial: {cls:'badge-partial', icon:'◑',label:'Partial — some features not implemented'}"),
  ("anatomic:{cls:'badge-anatomic',icon:'△',label:'Solo stadio anatomico — mancano parametri prognostici'}",
   "anatomic:{cls:'badge-anatomic',icon:'△',label:'Anatomic stage only — prognostic parameters not included'}"),
  ("verify:  {cls:'badge-verify',  icon:'!',label:'Richiede verifica manuale'}",
   "verify:  {cls:'badge-verify',  icon:'!',label:'Requires manual verification'}"),
  ("if(s.model_limited)html+=`<span class=\"badge badge-anat\">⚠ Modello ridotto</span>`;",
   "if(s.model_limited)html+=`<span class=\"badge badge-anat\">⚠ Reduced model</span>`;"),
  # renderLookup section titles
  ("'<div class=\"tnm-section\"><div class=\"section-title\">T — Tumore Primitivo</div>'",
   "'<div class=\"tnm-section\"><div class=\"section-title\">T — Primary Tumor</div>'"),
  ("'<div class=\"tnm-section\"><div class=\"section-title\">N — Linfonodi Regionali</div>'",
   "'<div class=\"tnm-section\"><div class=\"section-title\">N — Regional Lymph Nodes</div>'"),
  ("'<div class=\"tnm-section\"><div class=\"section-title\">M — Metastasi a Distanza</div>'",
   "'<div class=\"tnm-section\"><div class=\"section-title\">M — Distant Metastasis</div>'"),
  # Clinical notes label
  ('`<div class="note-box"><strong>⚠ Note cliniche:</strong> ${s.note}</div>`',
   '`<div class="note-box"><strong>⚠ Clinical notes:</strong> ${s.note}</div>`'),
  # Coverage
  ("T:'Categorie T',N:'Categorie N',M:'Categorie M',",
   "T:'T categories',N:'N categories',M:'M categories',"),
  ("stage:'Stage grouping',note_eccezioni:'Note/eccezioni',",
   "stage:'Stage grouping',note_eccezioni:'Notes/exceptions',"),
  ("soglia_pN0:'Soglia pN0',confini_anatomici:'Confini anatomici'",
   "soglia_pN0:'pN0 threshold',confini_anatomici:'Anatomic boundaries'"),
  ("COV_ICONS={ok:'✓ completo',partial:'◑ parziale',missing:'— non documentato'};",
   "COV_ICONS={ok:'✓ complete',partial:'◑ partial',missing:'— not documented'};"),
  ("'<div style=\"margin-top:16px\"><div class=\"section-title\">Copertura del modello</div>'",
   "'<div style=\"margin-top:16px\"><div class=\"section-title\">Model coverage</div>'"),
  ("'<table class=\"coverage-table\"><thead><tr><th>Campo</th><th>Stato</th></tr></thead><tbody>'",
   "'<table class=\"coverage-table\"><thead><tr><th>Field</th><th>Status</th></tr></thead><tbody>'"),
]

# ════════════════════════════════════════════════════════════════════════════
# 9. JS: computeStage strings
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("const stageHeader=currentSite?.model_limited?'Raggruppamento anatomico TNM':'Stadio';",
   "const stageHeader=currentSite?.model_limited?'Anatomic TNM grouping':'Stage';"),
  ("?'⛔ Ambiguità: '+result.allStages.join(' / ')+' — non assegnabile'",
   "?'⛔ Ambiguity: '+result.allStages.join(' / ')+' — not assignable'"),
  (":'⛔ Combinazione incoerente'",  ":'⛔ Inconsistent combination'"),
  ("stageLabel='Parametri incompleti — staging non assegnabile';",
   "stageLabel='Incomplete parameters — staging not assignable';"),
  ("stageLabel='Non determinabile (caso fuori modello)';",
   "stageLabel='Not determinable (case outside model)';"),
  ("stageQuality=v.warnings.length?' (con riserva)':' (assegnato)';",
   "stageQuality=v.warnings.length?' (with caveat)':' (assigned)';"),
  ("document.getElementById('stage-label').textContent='TNM 9ª Ed. · UICC 2025'+stageQuality;",
   "document.getElementById('stage-label').textContent='TNM 9th Ed. · UICC 2025'+stageQuality;"),
]

# ════════════════════════════════════════════════════════════════════════════
# 10. JS: generateReferto strings
# ════════════════════════════════════════════════════════════════════════════
R += [
  # TX/NX block messages
  ("if(stripPfx(_T)==='TX')_which.push('T non valutabile (TX)');",
   "if(stripPfx(_T)==='TX')_which.push('T not assessable (TX)');"),
  ("if(stripPfx(_N)==='NX')_which.push('N non valutabile (NX)');",
   "if(stripPfx(_N)==='NX')_which.push('N not assessable (NX)');"),
  ("_out2.textContent='⚠️ REFERTO NON GENERATO\\n\\n'+_which.join('\\n')+'\\n\\nLo stadio non può essere assegnato con parametri non valutabili.';",
   "_out2.textContent='⚠️ REPORT NOT GENERATED\\n\\n'+_which.join('\\n')+'\\n\\nStage cannot be assigned with non-assessable parameters.';"),
  # LN incongruent
  ("out.textContent='⚠️ REFERTO NON GENERATO\\n\\nDato incongruente: linfonodi positivi ('+_refPos+') > linfonodi esaminati ('+_refTot+').\\nCorreggere i dati prima di generare il referto.';",
   "out.textContent='⚠️ REPORT NOT GENERATED\\n\\nInconsistent data: positive lymph nodes ('+_refPos+') > examined lymph nodes ('+_refTot+').\\nCorrect the data before generating the report.';"),
  # Report header
  ("let txt=`CLASSIFICAZIONE TNM\\n`;",
   "let txt=`TNM CLASSIFICATION\\n`;"),
  ("txt+=`Riferimento: UICC TNM Classification of Malignant Tumours, 9ª ed. (2025) / AJCC Cancer Staging Manual, Version 9\\n`;",
   "txt+=`Reference: UICC TNM Classification of Malignant Tumours, 9th ed. (2025) / AJCC Cancer Staging Manual, Version 9\\n`;"),
  ("txt+=`Sede: ${s.name} (ICD-O-4: ${s.icd})\\n`;",
   "txt+=`Site: ${s.name} (ICD-O-4: ${s.icd})\\n`;"),
  ("txt+=`Variante/istotipo: ${varLabel}\\n`;",
   "txt+=`Variant/histotype: ${varLabel}\\n`;"),
  ("const stageHeader=s.model_limited?'RAGGRUPPAMENTO ANATOMICO TNM':'STADIO';",
   "const stageHeader=s.model_limited?'ANATOMIC TNM GROUPING':'STAGE';"),
  # Section headers
  ("txt+='\\n── CLASSIFICAZIONE TNM ──────────────────────────────────\\n';",
   "txt+='\\n── TNM CLASSIFICATION ───────────────────────────────────\\n';"),
  ("if(nTotN>0)nLine+=` (${nPosN} LN+ su ${nTotN} esaminati)`;",
   "if(nTotN>0)nLine+=` (${nPosN} LN+ out of ${nTotN} examined)`;"),
  # M source labels
  ("const mSourceLabel=mSource==='cM'?'clinico/radiologico':mSource==='pM'?'patologico (biopsia)':mSource==='ycM'?'post-trattamento, clinico/radiologico':mSource==='ypM'?'post-trattamento, patologico':'non documentato';",
   "const mSourceLabel=mSource==='cM'?'clinical/radiological':mSource==='pM'?'pathological (biopsy)':mSource==='ycM'?'post-treatment, clinical/radiological':mSource==='ypM'?'post-treatment, pathological':'not documented';"),
  ("mFullCode='M non assegnabile';",
   "mFullCode='M not assignable';"),
  ("mDesc='metastasi a distanza non documentata nel materiale disponibile';",
   "mDesc='distant metastasis not documented in available material';"),
  ("txt+=`         Nota M: valutazione ${mSourceLabel}\\n`;",
   "txt+=`         M note: assessment ${mSourceLabel}\\n`;"),
  ("txt+=`Parametri aggiuntivi: ${extraKeys.map(k=>k+'='+extra[k]).join(', ')}\\n`;",
   "txt+=`Additional parameters: ${extraKeys.map(k=>k+'='+extra[k]).join(', ')}\\n`;"),
  ("txt+='\\n── RAGGRUPPAMENTO DI STADIO ─────────────────────────────\\n';",
   "txt+='\\n── STAGE GROUPING ───────────────────────────────────────\\n';"),
  # Prostate footnote
  ("'\\n⚠ ATTENZIONE: questo NON corrisponde al Prognostic Stage Group. Per la prostata il gruppo prognostico formale richiede PSA (ng/mL) e Grade Group (Gleason score). Integrare con questi dati prima di qualsiasi uso clinico.'",
   "'\\n⚠ WARNING: this does NOT correspond to the Prognostic Stage Group. For prostate, the formal prognostic group requires PSA (ng/mL) and Grade Group (Gleason score). Integrate these data before any clinical use.'"),
  # Stage quality
  ("stageQualityLabel='NON ASSEGNABILE — combinazione incoerente (vedi avvertenze)';",
   "stageQualityLabel='NOT ASSIGNABLE — inconsistent combination (see warnings)';"),
  ("stageQualityLabel='NON ASSEGNABILE — parametri incompleti (vedi avvertenze)';",
   "stageQualityLabel='NOT ASSIGNABLE — incomplete parameters (see warnings)';"),
  ("stageQualityLabel='NON DETERMINABILE — caso fuori modello o classificazione non applicabile';",
   "stageQualityLabel='NOT DETERMINABLE — case outside model or classification not applicable';"),
  ("stageQualityLabel=stage+' (assegnato con riserva — vedi avvertenze)';",
   "stageQualityLabel=stage+' (assigned with caveat — see warnings)';"),
  ("stageQualityLabel=stage+' (assegnato)';",
   "stageQualityLabel=stage+' (assigned)';"),
  # Validation prefixes in report
  ("...v.errors.map(e=>'⛔ INCOERENZA: '+e),",
   "...v.errors.map(e=>'⛔ INCONSISTENCY: '+e),"),
  ("...v.incomplete.map(e=>'⚠ INCOMPLETO: '+e),",
   "...v.incomplete.map(e=>'⚠ INCOMPLETE: '+e),"),
  ("...v.warnings.map(e=>'📋 NOTA: '+e),",
   "...v.warnings.map(e=>'📋 NOTE: '+e),"),
  ("if(notes)txt+=`\\nNote: ${notes}`;",
   "if(notes)txt+=`\\nNotes: ${notes}`;"),
  # Prognostic factors
  ("txt+='\\n── FATTORI PROGNOSTICI / PREDITTIVI ────────────────────\\n';",
   "txt+='\\n── PROGNOSTIC / PREDICTIVE FACTORS ─────────────────────\\n';"),
  ("txt+='(Non inclusi nel raggruppamento TNM — riportati a fini clinici)\\n';",
   "txt+='(Not included in TNM grouping — reported for clinical purposes)\\n';"),
  # Footer
  ("txt+=`\\n\\n[Stadio preliminare — Verificare sempre con la fonte primaria: TNM Classification of Malignant Tumours, 9ª Ed., UICC 2025]`;",
   "txt+=`\\n\\n[Preliminary staging — Always verify against the primary source: TNM Classification of Malignant Tumours, 9th Ed., UICC 2025]`;"),
]

# ════════════════════════════════════════════════════════════════════════════
# 11. JS: copyReferto, lnCrossCheck, autoCalcN, renderValidation
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("btn.textContent='✅ Copiato!';", "btn.textContent='✅ Copied!';"),
  ("setTimeout(()=>{btn.textContent='📋 Copia negli Appunti';},2000);",
   "setTimeout(()=>{btn.textContent='📋 Copy to Clipboard';},2000);"),
  # lnCrossCheck (appears twice - staging + referto)
  ("warn.textContent='⚠️ LN positivi ('+pos+') > LN esaminati ('+tot+') — dato incongruente';",
   "warn.textContent='⚠️ LN positive ('+pos+') > LN examined ('+tot+') — inconsistent data';"),
  # autoCalcN badges
  ("badge.textContent='⟵ suggerito: '+nPos+'LN+ '+(dimStr?'dim.'+dimStr:'');",
   "badge.textContent='⟵ suggested: '+nPos+'LN+ '+(dimStr?'dim.'+dimStr:'');"),
  ("badge.textContent='⟵ suggerito da LN+: '+nPos;",
   "badge.textContent='⟵ suggested from LN+: '+nPos;"),
  # renderValidation
  ('html+=`<div class="v-error"><div class="v-label">⛔ Combinazione incoerente</div>${v.errors.map(e=>\'• \'+e).join(\'<br>\')}</div>`;',
   'html+=`<div class="v-error"><div class="v-label">⛔ Inconsistent combination</div>${v.errors.map(e=>\'• \'+e).join(\'<br>\')}</div>`;'),
  ('html+=`<div class="v-incomplete"><div class="v-label">⚠ Dato mancante / staging non assegnabile</div>${v.incomplete.map(e=>\'• \'+e).join(\'<br>\')}</div>`;',
   'html+=`<div class="v-incomplete"><div class="v-label">⚠ Missing data / staging not assignable</div>${v.incomplete.map(e=>\'• \'+e).join(\'<br>\')}</div>`;'),
  ('html+=`<div class="v-warning"><div class="v-label">📋 Note cliniche</div>${v.warnings.map(e=>\'• \'+e).join(\'<br>\')}</div>`;',
   'html+=`<div class="v-warning"><div class="v-label">📋 Clinical notes</div>${v.warnings.map(e=>\'• \'+e).join(\'<br>\')}</div>`;'),
  # staging type bar label
  ("<span style=\"font-size:10px;opacity:.7;text-transform:uppercase;letter-spacing:.5px\">Tipo staging:</span>",
   "<span style=\"font-size:10px;opacity:.7;text-transform:uppercase;letter-spacing:.5px\">Staging type:</span>"),
]

# ════════════════════════════════════════════════════════════════════════════
# 12. JS: validateCase messages
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("incomplete.push('T non valutabile (TX): lo stadio non può essere assegnato. Rivalutare il campione o indicare il motivo della non valutabilità.');",
   "incomplete.push('T not assessable (TX): stage cannot be assigned. Re-evaluate the specimen or document the reason for non-assessability.');"),
  ("incomplete.push('N non valutabile (NX): lo stadio non può essere assegnato. Specificare il numero di linfonodi esaminati o il motivo della non valutabilità.');",
   "incomplete.push('N not assessable (NX): stage cannot be assigned. Specify the number of examined lymph nodes or document the reason for non-assessability.');"),
  ("errors.push('Tis con '+N+': combinazione biologicamente incongruente. Verificare la classificazione T o la presenza di un secondo focolaio invasivo.');",
   "errors.push('Tis with '+N+': biologically inconsistent combination. Verify T classification or presence of a second invasive focus.');"),
  ("errors.push('N0 è incompatibile con '+nPos+' linfonodi positivi dichiarati.');",
   "errors.push('N0 is incompatible with '+nPos+' declared positive lymph nodes.');"),
  ("errors.push('N1c in questa sede ('+site.name+') indica depositi tumorali senza metastasi linfonodali; incompatibile con '+nPos+' linfonodi positivi dichiarati. Rivalutare la categoria N.');",
   "errors.push('N1c at this site ('+site.name+') indicates tumor deposits without lymph node metastases; incompatible with '+nPos+' declared positive lymph nodes. Re-evaluate N category.');"),
  ("errors.push('Il numero di linfonodi positivi ('+nPos+') supera il totale esaminato ('+nTot+'). Dati incongruenti.');",
   "errors.push('Number of positive lymph nodes ('+nPos+') exceeds total examined ('+nTot+'). Inconsistent data.');"),
  ("errors.push('Categoria N incongruente: con '+nPosVal+' LN+ attesa '+expectedN+', selezionata '+nCode+'. Correggere o usare l\\'auto-calcolo LN+.');",
   "errors.push('Inconsistent N category: with '+nPosVal+' LN+ expected '+expectedN+', selected '+nCode+'. Correct or use the LN+ auto-calculation.');"),
  ("warnings.push('Categoria pN selezionata senza numero di linfonodi esaminati documentato.');",
   "warnings.push('pN category selected without documented number of examined lymph nodes.');"),
  ("warnings.push('pN0 con campionamento potenzialmente inadeguato: '+nTot+' linfonodi esaminati (minimo raccomandato per questa sede: '+minLN+'). Riportare il numero; la categoria rimane pN0 con riserva.');",
   "warnings.push('pN0 with potentially inadequate sampling: '+nTot+' lymph nodes examined (recommended minimum for this site: '+minLN+'). Report the number; category remains pN0 with caveat.');"),
  ("warnings.push('Canale anale pN0: il minimo raccomandato è ≥12 LN per la dissezione perirettale/pelvica e ≥6 LN per la dissezione inguinale. Con '+nTot+' LN esaminati verificare il territorio di dissezione.');",
   "warnings.push('Anal canal pN0: recommended minimum is ≥12 LN for perirectal/pelvic dissection and ≥6 LN for inguinal dissection. With '+nTot+' LN examined, verify the dissection territory.');"),
  ("warnings.push('Prostata: lo stadio mostrato è il raggruppamento anatomico (T/N/M). Il gruppo prognostico formale richiede anche PSA e Grade Group (Gleason). Per la documentazione clinica includere entrambi.');",
   "warnings.push('Prostate: stage shown is anatomic grouping (T/N/M). Formal prognostic group also requires PSA and Grade Group (Gleason). Include both for clinical documentation.');"),
  ("incomplete.push('M1b appendice: il grado istologico è determinante per IVA (G1) vs IVB (G2/G3/GX). Selezionare il grado.');",
   "incomplete.push('M1b appendix: histological grade determines IVA (G1) vs IVB (G2/G3/GX). Please select the grade.');"),
  ("warnings.push('S=SX: marcatori sierici non disponibili/non eseguiti. Stadio assegnato come Stage I generico (senza sottostadio IA/IB/IS). Per l\\'assegnazione formale registrare il nadir post-orchidectomia di AFP, hCG e LDH.');",
   "warnings.push('S=SX: serum markers not available/not performed. Stage assigned as generic Stage I (without substage IA/IB/IS). For formal assignment, document post-orchiectomy nadir AFP, hCG and LDH.');"),
  ("warnings.push('Per M1a (solo mucina acellulare) il grado non influenza lo stadio (sempre IVA). Il campo grado è rilevante solo per M1b.');",
   "warnings.push('For M1a (acellular mucin only) grade does not influence the stage (always IVA). The grade field is only relevant for M1b.');"),
  ("warnings.push('Esofago: i gruppi prognostici con grado (Pathological Prognostic Groups) non sono implementati in questo motore. Lo staging mostrato è lo Stage Group anatomico senza correzione per grado e sede anatomica del tumore.');",
   "warnings.push('Esophagus: grade-based prognostic groups (Pathological Prognostic Groups) are not implemented in this tool. The stage shown is the anatomic Stage Group without correction for tumor grade and anatomic location.');"),
  ("warnings.push('Mammella: N0(i+)/N0(mol+)/cM0(i+) non modificano il raggruppamento di stadio (rimane N0/M0 per le regole di staging). Riportare nel referto come dato biologico aggiuntivo.');",
   "warnings.push('Breast: N0(i+)/N0(mol+)/cM0(i+) do not modify the stage grouping (remains N0/M0 for staging rules). Report in the pathology note as an additional biological finding.');"),
  ("warnings.push('Tis(LCIS) — divergenza UICC/AJCC: UICC TNM 9ª ed. include questa categoria nello Stadio 0; AJCC Cancer Staging Manual, 8ª ed. / Version 9 la esclude. Staging mostrato: UICC. Non classificabile formalmente secondo AJCC.');",
   "warnings.push('Tis(LCIS) — UICC/AJCC divergence: UICC TNM 9th ed. includes this category in Stage 0; AJCC Cancer Staging Manual Version 9 excludes it. Stage shown: UICC. Not formally classifiable per AJCC.');"),
  ("warnings.push(\"T3 pelvi renale include l'invasione del parenchima renale — può simulare RCC primitivo in campione frammentato. Verificare IHC se necessario (GATA3+/CK7+ vs CD10+/CK7-).\");",
   "warnings.push(\"T3 renal pelvis includes renal parenchymal invasion — may mimic primary RCC in fragmented specimens. Verify IHC if needed (GATA3+/CK7+ vs CD10+/CK7-).\");"),
  ("warnings.push('Uretra: staging usa codici T differenziati per sesso (T2M/T3M/T4M per maschile; T2F/T3F/T4F per femminile). Verificare che la variante selezionata corrisponda al sesso del paziente.');",
   "warnings.push('Urethra: staging uses sex-differentiated T codes (T2M/T3M/T4M for male; T2F/T3F/T4F for female). Verify that the selected variant matches the patient sex.');"),
  ("warnings.push('Dimensione metastasi ≤0.2 mm: classificare come N0(i+) — ITC (cellule tumorali isolate). Non equivale a N1mi (≤0.2–2 mm). Indicare esplicitamente nel referto.');",
   "warnings.push('Metastasis size ≤0.2 mm: classify as N0(i+) — ITC (isolated tumor cells). Not equivalent to N1mi (0.2–2 mm). Explicitly state in the report.');"),
  ("warnings.push('Dimensione metastasi >0.2 e ≤2 mm: corrisponde a N1mi (micrometastasi). Verificare la categoria N selezionata.');",
   "warnings.push('Metastasis size >0.2 and ≤2 mm: corresponds to N1mi (micrometastasis). Verify the selected N category.');"),
  # ambiguity (appears in both computeStage and generateReferto)
  ("v.errors.push('Ambiguità dataset: stadi '+result.allStages.join(' / ')+' compatibili simultaneamente — staging non assegnabile. Segnalare il bug.');",
   "v.errors.push('Dataset ambiguity: stages '+result.allStages.join(' / ')+' simultaneously compatible — staging not assignable. Please report the bug.');"),
]

# ════════════════════════════════════════════════════════════════════════════
# 13. SITE NAMES
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("name:'Colon e Retto'",           "name:'Colorectum'"),
  ("name:'Stomaco'",                 "name:'Stomach'"),
  ("name:'Esofago / GEJ'",           "name:'Esophagus / GEJ'"),
  ("name:'Intestino Tenue'",         "name:'Small Intestine'"),
  ("name:'Appendice'",               "name:'Appendix'"),
  ("name:'Canale Anale'",            "name:'Anal Canal'"),
  ("name:'Fegato (HCC)'",            "name:'Liver (HCC)'"),
  ("name:'Dotti biliari intraepatici (CCA)'", "name:'Intrahepatic Bile Ducts (CCA)'"),
  ("name:'Vie biliari periilari (Klatskin)'", "name:'Perihilar Bile Ducts (Klatskin)'"),
  ("name:'Via biliare distale'",     "name:'Distal Bile Duct'"),
  ("name:'Colecisti'",               "name:'Gallbladder'"),
  ("name:'Ampolla di Vater'",        "name:'Ampulla of Vater'"),
  ("name:'NET GI — Stomaco'",        "name:'GI NET — Stomach'"),
  ("name:'NET GI — Colon-Retto'",    "name:'GI NET — Colorectum'"),
  ("name:'NET GI — Pancreas'",       "name:'GI NET — Pancreas'"),
  ("name:'Tiroide'",                 "name:'Thyroid'"),
  ("name:'Ghiandole salivari'",      "name:'Salivary Glands'"),
  ("name:'Mammella'",                "name:'Breast'"),
  ("name:'Prostata'",                "name:'Prostate'"),
  ("name:'Vescica'",                 "name:'Bladder'"),
  ("name:'Rene (RCC)'",              "name:'Kidney (RCC)'"),
  ("name:'Testicolo'",               "name:'Testis'"),
  ("name:'Pelvi Renale'",            "name:'Renal Pelvis'"),
  ("name:'Uretere'",                 "name:'Ureter'"),
  ("name:'Uretra'",                  "name:'Urethra'"),
  ("name:'Melanoma cutaneo'",        "name:'Cutaneous Melanoma'"),
  ("name:'Carcinoma della cute'",    "name:'Skin Carcinoma'"),
  ("name:'Carcinoma di Merkel'",     "name:'Merkel Cell Carcinoma'"),
]

# ════════════════════════════════════════════════════════════════════════════
# 14. SITE staging_type_label strings
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("staging_type_label:'Stadio anatomico UICC'",       "staging_type_label:'UICC anatomic stage'"),
  ("staging_type_label:'Varianti clinico/patologico'", "staging_type_label:'Clinical/pathological variants'"),
  ("staging_type_label:'4 varianti (SCC/Adeno × cStage/pStage) — PPG con grado/sede non implementati (AJCC v9)'",
   "staging_type_label:'4 variants (SCC/Adeno × cStage/pStage) — PPG with grade/location not implemented (AJCC v9)'"),
  ("staging_type_label:'Stadio anatomico UICC — solo HCC'", "staging_type_label:'UICC anatomic stage — HCC only'"),
  ("staging_type_label:'Stadio anatomico UICC — solo CCA'", "staging_type_label:'UICC anatomic stage — CCA only'"),
  ("staging_type_label:'Stadio anatomico UICC — Klatskin (V9)'", "staging_type_label:'UICC anatomic stage — Klatskin (V9)'"),
  ("staging_type_label:'Stadio anatomico UICC — via biliare distale'", "staging_type_label:'UICC anatomic stage — distal bile duct'"),
  ("staging_type_label:'Stadio anatomico UICC — colecisti'", "staging_type_label:'UICC anatomic stage — gallbladder'"),
  ("staging_type_label:'Stadio anatomico UICC — ampolla di Vater'", "staging_type_label:'UICC anatomic stage — ampulla of Vater'"),
  ("staging_type_label:'Stadio anatomico UICC — adenocarcinoma'", "staging_type_label:'UICC anatomic stage — adenocarcinoma'"),
  ("staging_type_label:'WHO 2022 · AJCC v9 · Grado come parametro T'", "staging_type_label:'WHO 2022 · AJCC v9 · Grade as T parameter'"),
  ("staging_type_label:'4 varianti (PTC/FTC ×<55aa/≥55aa, midollare, anaplastico)'",
   "staging_type_label:'4 variants (PTC/FTC × <55yr/≥55yr, medullary, anaplastic)'"),
  ("staging_type_label:'Varianti cN/pN — schema ENE-based V9'", "staging_type_label:'cN/pN variants — V9 ENE-based schema'"),
  ("staging_type_label:'Anatomico UICC — Prognostic Stage AJCC non implementato'",
   "staging_type_label:'UICC anatomic — AJCC Prognostic Stage not implemented'"),
  ("staging_type_label:'Solo anatomico — PSA/Grade Group non implementati'",
   "staging_type_label:'Anatomic only — PSA/Grade Group not implemented'"),
  ("staging_type_label:'Stadio anatomico UICC'",  "staging_type_label:'UICC anatomic stage'"),
  ("staging_type_label:'Stadio anatomico AJCC v9'", "staging_type_label:'AJCC v9 anatomic stage'"),
  ("staging_type_label:'Stadio anatomico UICC — solo RCC'", "staging_type_label:'UICC anatomic stage — RCC only'"),
  ("staging_type_label:'Anatomico UICC con marcatori S'", "staging_type_label:'UICC anatomic with S markers'"),
  ("staging_type_label:'Varianti M/F — codici T differenziati'", "staging_type_label:'M/F variants — sex-differentiated T codes'"),
  ("staging_type_label:'Stadio clinico e patologico — LDH substaging non implementato'",
   "staging_type_label:'Clinical and pathological stage — LDH substaging not implemented'"),
  ("staging_type_label:'Stadio anatomico UICC — SCC/BCC'", "staging_type_label:'UICC anatomic stage — SCC/BCC'"),
  ("staging_type_label:'Stadio anatomico UICC — Merkel'", "staging_type_label:'UICC anatomic stage — Merkel'"),
]

# ════════════════════════════════════════════════════════════════════════════
# 15. SITE variant labels
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("{id:'clinical',label:'Stadio clinico (cTNM)'}",    "{id:'clinical',label:'Clinical stage (cTNM)'}"),
  ("{id:'path',label:'Stadio patologico (pTNM)'}",     "{id:'path',label:'Pathological stage (pTNM)'}"),
  ("{id:'path',label:'pN — Stadiazione patologica'}",  "{id:'path',label:'pN — Pathological staging'}"),
  ("{id:'clinical',label:'cN — Stadiazione clinica'}", "{id:'clinical',label:'cN — Clinical staging'}"),
  ("{id:'scc_path',label:'SCC — pStage'}",   "{id:'scc_path',label:'SCC — pStage'}"),
  ("{id:'scc_clin',label:'SCC — cStage'}",   "{id:'scc_clin',label:'SCC — cStage'}"),
  ("{id:'adeno_path',label:'Adeno — pStage'}", "{id:'adeno_path',label:'Adeno — pStage'}"),
  ("{id:'adeno_clin',label:'Adeno — cStage'}", "{id:'adeno_clin',label:'Adeno — cStage'}"),
  # Thyroid variants
  ("{id:'ptc_ftc_young',label:'PTC/FTC <55 anni'}", "{id:'ptc_ftc_young',label:'PTC/FTC <55 years'}"),
  ("{id:'ptc_ftc_old',label:'PTC/FTC ≥55 anni'}",  "{id:'ptc_ftc_old',label:'PTC/FTC ≥55 years'}"),
  ("{id:'medullary',label:'Midollare (MTC)'}",       "{id:'medullary',label:'Medullary (MTC)'}"),
  ("{id:'anaplastic',label:'Anaplastico (ATC)'}",    "{id:'anaplastic',label:'Anaplastic (ATC)'}"),
  # Prostate
  ("{id:'clinical',label:'Stadio clinico'}",   "{id:'clinical',label:'Clinical stage'}"),
  ("{id:'path',label:'Stadio patologico'}",     "{id:'path',label:'Pathological stage'}"),
  # Melanoma
  ("{id:'clinical',label:'Stadio clinico (cTNM) — LDH substaging non implementato'}",
   "{id:'clinical',label:'Clinical stage (cTNM) — LDH substaging not implemented'}"),
  ("{id:'path',label:'Stadio patologico (pTNM) — LDH substaging non implementato'}",
   "{id:'path',label:'Pathological stage (pTNM) — LDH substaging not implemented'}"),
  # Urethra
  ("{id:'maschile',label:'Uretra maschile'}", "{id:'maschile',label:'Male urethra'}"),
  ("{id:'femminile',label:'Uretra femminile'}", "{id:'femminile',label:'Female urethra'}"),
]

# ════════════════════════════════════════════════════════════════════════════
# 16. SITE EXTRA field labels
# ════════════════════════════════════════════════════════════════════════════
R += [
  ("label:'Grado istologico (rilevante per M1b)'", "label:'Histological grade (relevant for M1b)'"),
  ("label:'Marcatori sierici (nadir post-orchidectomia)'",
   "label:'Serum markers (post-orchiectomy nadir)'"),
]

# ════════════════════════════════════════════════════════════════════════════
# 17. T DESCRIPTIONS — common patterns (applied broadly)
# ════════════════════════════════════════════════════════════════════════════
# These patterns appear across many sites; apply them to all d: fields
T_PATTERNS = [
  # Standard TX/T0
  ("Tumore primitivo non valutabile", "Primary tumor not assessable"),
  ("Nessuna evidenza di tumore primitivo", "No evidence of primary tumor"),
  # Generic non-assessable
  ("Non valutabile", "Not assessable"),
  ("Non valutabili", "Not assessable"),
  ("Nessun tumore", "No tumor"),
  # Carcinoma in situ - same in both languages, skip
  # Invasion verbs
  ("Tumore che invade la lamina propria o la muscularis mucosae",
   "Tumor invading the lamina propria or muscularis mucosae"),
  ("Tumore che invade la lamina propria",    "Tumor invading the lamina propria"),
  ("Tumore che invade la muscularis mucosae","Tumor invading the muscularis mucosae"),
  ("Tumore che invade la sottomucosa",       "Tumor invading the submucosa"),
  ("Tumore che invade la muscularis propria","Tumor invading the muscularis propria"),
  ("Tumore che invade la muscularis propria superficiale (metà interna)",
   "Tumor invading the superficial muscularis propria (inner half)"),
  ("Tumore che invade la muscularis propria profonda (metà esterna)",
   "Tumor invading the deep muscularis propria (outer half)"),
  ("Tumore che invade la sottosierosa",      "Tumor invading the subserosa"),
  ("Tumore che perfora il peritoneo viscerale","Tumor perforating the visceral peritoneum"),
  ("Tumore che perfora la sierosa (peritoneo viscerale)","Tumor perforating the serosa (visceral peritoneum)"),
  ("Tumore che invade direttamente altri organi o strutture",
   "Tumor directly invading other organs or structures"),
  ("Tumore che invade il tessuto connettivo sottoepiteliale",
   "Tumor invading the subepithelial connective tissue"),
  ("Tumore che invade strutture adiacenti", "Tumor invading adjacent structures"),
  ("Tumore che invade", "Tumor invading"),
  # Invade (lowercase)
  ("Invade la lamina propria o la muscularis mucosae",
   "Invading the lamina propria or muscularis mucosae"),
  ("Invade la lamina propria",     "Invading the lamina propria"),
  ("Invade la sottomucosa",        "Invading the submucosa"),
  ("Invade la muscularis propria", "Invading the muscularis propria"),
  ("Invade la sottosierosa",       "Invading the subserosa"),
  ("Invade direttamente",          "Directly invading"),
  ("Perfora il peritoneo viscerale","Perforating the visceral peritoneum"),
  ("invade la lamina propria",     "invading the lamina propria"),
  ("invade la sottomucosa",        "invading the submucosa"),
  ("invade la muscularis propria", "invading the muscularis propria"),
  ("invade la sottosierosa",       "invading the subserosa"),
  ("invade il tessuto connettivo", "invading the connective tissue"),
  ("invade direttamente",          "directly invading"),
  ("perfora il peritoneo viscerale","perforating the visceral peritoneum"),
  ("perfora la sierosa",           "perforating the serosa"),
  # Size
  ("nella dimensione maggiore",    "in greatest dimension"),
  ("dimensione maggiore",          "greatest dimension"),
  # Vascular
  ("senza invasione vascolare",    "without vascular invasion"),
  ("con invasione vascolare e",    "with vascular invasion and"),
  ("con invasione vascolare",      "with vascular invasion"),
  # Solitary/multiple
  ("Tumore solitario",             "Solitary tumor"),
  ("Tumori multipli",              "Multiple tumors"),
  ("nessuno",                      "none"),
  # Organs / structures (in T descriptions)
  ("tessuto connettivo sottoepiteliale",  "subepithelial connective tissue"),
  ("tessuto perivescicale",        "perivesical tissue"),
  ("tessuto perimuscolare",        "perimuscular tissue"),
  ("peritoneo viscerale",          "visceral peritoneum"),
  ("muscularis mucosae",           "muscularis mucosae"),
  ("muscularis propria",           "muscularis propria"),
  ("lamina propria",               "lamina propria"),
  ("sottomucosa",                  "submucosa"),
  ("sottosierosa",                 "subserosa"),
  ("avventizia",                   "adventitia"),
  ("grasso periesofageo",          "periesophageal fat"),
  ("mesoappendice",                "mesoappendix"),
  ("mesentere",                    "mesentery"),
  ("retroperitoneo",               "retroperitoneum"),
  ("parete addominale",            "abdominal wall"),
  ("parete pelvica",               "pelvic wall"),
  ("parete rettale",               "rectal wall"),
  ("stroma prostatico",            "prostatic stroma"),
  ("vescichette seminali",         "seminal vesicles"),
  ("sfintere esterno",             "external sphincter"),
  ("muscoli elevatori",            "levator muscles"),
  ("capsula prostatica",           "prostatic capsule"),
  ("corpo spongioso",              "corpus spongiosum"),
  ("corpo cavernoso",              "corpus cavernosum"),
  ("canale uditivo",               "auditory canal"),
  ("nervo facciale",               "facial nerve"),
  ("nervo facciale VII",           "facial nerve (VII)"),
  ("base cranica",                 "skull base"),
  ("placche pterigoidee",          "pterygoid plates"),
  ("arteria carotide",             "carotid artery"),
  ("arteria epatica propria",      "proper hepatic artery"),
  ("arteria epatica",              "hepatic artery"),
  ("vena porta",                   "portal vein"),
  ("vena epatica",                 "hepatic vein"),
  ("vena cava inferiore",          "inferior vena cava"),
  ("vena azygos",                  "azygos vein"),
  ("vena azigos",                  "azygos vein"),
  ("diaframma inferiore",          "inferior diaphragm"),
  ("diaframma",                    "diaphragm"),
  ("pericardio",                   "pericardium"),
  ("pleura",                       "pleura"),
  ("trachea",                      "trachea"),
  ("aorta",                        "aorta"),
  ("corpo vertebrale",             "vertebral body"),
  ("colon trasverso",              "transverse colon"),
  ("ampolla di Vater",             "ampulla of Vater"),
  ("ilo epatico",                  "hepatic hilum"),
  ("parenchima renale",            "renal parenchyma"),
  ("pelvi renale",                 "renal pelvis"),
  ("uretra prostatica",            "prostatic urethra"),
  ("parete anteriore della vescica","anterior bladder wall"),
  ("parete anteriore della vagina", "anterior vaginal wall"),
  ("collo vescicale",              "bladder neck"),
  ("cute del perineo",             "perineal skin"),
  ("parenchima epatico",           "hepatic parenchyma"),
  # Specific descriptors
  ("extraparenchimale",            "extraparenchymal"),
  ("extraprostatica",              "extraprostatic"),
  ("unilaterale o bilaterale",     "unilateral or bilateral"),
  ("incluso il coinvolgimento microscopico del collo vescicale",
   "including microscopic involvement of the bladder neck"),
  ("inclusa la cute perianale",    "including perianal skin"),
  ("adiacenti eccetto la colecisti","adjacent except the gallbladder"),
  ("con perforazione del peritoneo viscerale","with perforation of the visceral peritoneum"),
  ("del parenchima mammario sottostante","of the underlying breast parenchyma"),
  ("del capezzolo",                "of the nipple"),
  ("della cute",                   "of the skin"),
  ("della sierosa",                "of the serosa"),
  ("del peritoneo",                "of the peritoneum"),
  ("con o senza invasione vascolare","with or without vascular invasion"),
  ("con o senza coinvolgimento",   "with or without involvement"),
  ("con estensione ≤2 cm",         "with extension ≤2 cm"),
  ("senza perforazione della sierosa","without serosal perforation"),
  ("senza estensione attraverso la muscularis mucosae",
   "without extension through the muscularis mucosae"),
  ("senza estensione extraparenchimale","without extraparenchymal extension"),
  ("cellule confinate alla lamina propria","cells confined to the lamina propria"),
  ("invasione della lamina propria","invasion of the lamina propria"),
  ("displasia di alto grado",      "high-grade dysplasia"),
  ("ad ago",                       "needle"),
  ("per PSA elevato",              "for elevated PSA"),
  ("nel ≤5% del tessuto resecato", "in ≤5% of the resected tissue"),
  ("in >5% del tessuto resecato",  "in >5% of the resected tissue"),
  ("identificato mediante biopsia", "identified by biopsy"),
  ("Riscontro istologico incidentale","Incidental histological finding"),
  ("la metà o meno di un lobo",    "one-half or less of one lobe"),
  ("più della metà di un lobo",    "more than one-half of one lobe"),
  ("ma non entrambi i lobi",       "but not both lobes"),
  ("entrambi i lobi",              "both lobes"),
  ("fisso o che invade",           "fixed or invading"),
  ("strutture diverse dalle",      "structures other than"),
  # Other Italian phrases in T descriptions
  ("invasione microscopica del tessuto perivescicale","microscopic invasion of the perivesical tissue"),
  ("invasione macroscopica del tessuto perivescicale (massa extravescicale)",
   "macroscopic invasion of the perivesical tissue (extravesical mass)"),
  ("Carcinoma papillare non invasivo","Non-invasive papillary carcinoma"),
  ("Carcinoma papillare/verrucoso/condilomatoso non invasivo",
   "Non-invasive papillary/verrucous/condylomatous carcinoma"),
  ("carcinoma infiammatorio",      "inflammatory carcinoma"),
  ("eritema diffuso e edema",      "diffuse erythema and edema"),
  ("che coinvolge ≥1/3 della mammella","involving ≥1/3 of the breast"),
  ("con esordio rapido",           "with rapid onset"),
  ("edema cutaneo (incluso peau d'orange)","skin edema (including peau d'orange)"),
  ("noduli cutanei satelliti omolaterali","ipsilateral satellite skin nodules"),
  ("Ulcerazione della cute",       "Skin ulceration"),
  ("Estensione alla parete toracica","Extension to the chest wall"),
  ("esclusa invasione isolata della muscolatura pettorale",
   "excluding isolated invasion of the pectoral muscle"),
  ("in assenza di criteri per carcinoma infiammatorio",
   "in the absence of criteria for inflammatory carcinoma"),
  ("Malattia di Paget del capezzolo","Paget disease of the nipple"),
  ("non associata a carcinoma invasivo o in situ",
   "not associated with invasive or in situ carcinoma"),
  ("Microinvasione",               "Microinvasion"),
  # Thyroid-specific
  ("Tumore ≤2 cm nella dimensione maggiore, confinato alla tiroide",
   "Tumor ≤2 cm in greatest dimension, confined to the thyroid"),
  ("Tumore >2 cm e ≤4 cm nella dimensione maggiore, confinato alla tiroide",
   "Tumor >2 cm and ≤4 cm in greatest dimension, confined to the thyroid"),
  ("Tumore >4 cm confinato alla tiroide",
   "Tumor >4 cm confined to the thyroid"),
  ("Estensione minima extratiroidea",
   "Minor extrathyroidal extension"),
  ("Estensione extratiroidea macroscopica",
   "Major extrathyroidal extension"),
  ("confinato alla tiroide",       "confined to the thyroid"),
  ("tessuti molli peritiroidei",   "perithyroidal soft tissues"),
  ("muscolo sternoioideo",         "sternohyoid muscle"),
  ("muscolo sternotiroideo",       "sternothyroid muscle"),
  ("muscoli del collo",            "strap muscles"),
  ("Qualsiasi T",                  "Any T"),
  ("qualsiasi T",                  "any T"),
  # Renal
  ("limitato al rene",             "limited to the kidney"),
  ("limitato al rene ≤7 cm",       "limited to the kidney, ≤7 cm"),
  ("limitato al rene >7 cm",       "limited to the kidney, >7 cm"),
  ("Tumore limitato al rene",      "Tumor limited to the kidney"),
  ("Estensione al grasso del seno renale o perirenale",
   "Extension into renal sinus fat or perirenal fat"),
  ("al grasso perirenale",         "into perirenal fat"),
  ("al grasso del seno renale",    "into renal sinus fat"),
  ("senza invasione della fascia di Gerota",
   "without invasion of the Gerota fascia"),
  ("Estensione alla vena renale",  "Extension into the renal vein"),
  ("alla vena cava sotto il diaframma","into the vena cava below the diaphragm"),
  ("alla vena cava sopra il diaframma","into the vena cava above the diaphragm"),
  ("fascia di Gerota",             "Gerota fascia"),
  ("ghiandola surrenale omolaterale","ipsilateral adrenal gland"),
  ("surrenale omolaterale",        "ipsilateral adrenal gland"),
  # Melanoma specific
  ("Spessore di Breslow",          "Breslow thickness"),
  ("spessore di Breslow",          "Breslow thickness"),
  ("ulcerazione",                  "ulceration"),
  ("con ulcerazione",              "with ulceration"),
  ("senza ulcerazione",            "without ulceration"),
  ("Melanoma in situ",             "Melanoma in situ"),
  ("≤0.8 mm senza ulcerazione",    "≤0.8 mm without ulceration"),
  ("≤0.8 mm con ulcerazione",      "≤0.8 mm with ulceration"),
  (">0.8 mm e ≤1 mm",              ">0.8 mm and ≤1 mm"),
  (">1 mm e ≤2 mm",                ">1 mm and ≤2 mm"),
  (">2 mm e ≤4 mm",                ">2 mm and ≤4 mm"),
  (">4 mm",                        ">4 mm"),
  ("Tumore primitivo non identificabile", "Primary tumor not identifiable"),
  # NET specific
  ("Tumore ≤1 cm confinato alla mucosa/sottomucosa",
   "Tumor ≤1 cm confined to the mucosa/submucosa"),
  ("Tumore >1 cm e ≤2 cm",         "Tumor >1 cm and ≤2 cm"),
  ("Tumore >2 cm o con invasione della sottomucosa profonda",
   "Tumor >2 cm or with deep submucosal invasion"),
  ("o con invasione della muscolare propria o della sottosierosa",
   "or with muscularis propria or subserosa invasion"),
  ("Invasione degli organi adiacenti","Invasion of adjacent organs"),
  # Bile duct specific
  ("invasione dei vasi portali",   "portal vessel invasion"),
  ("della vena porta",             "of the portal vein"),
  ("Tumore limitato al dotto biliare con invasione fino alla tonaca muscolare o al tessuto fibroso",
   "Tumor limited to the bile duct with invasion up to the muscularis or fibrous tissue"),
  ("Tumore che invade al di là della parete del dotto biliare",
   "Tumor invading beyond the wall of the bile duct"),
  ("con invasione dei tessuti adiposi pericolecistitici",
   "with invasion of the pericholecystic adipose tissue"),
  # Common adjectival forms
  ("bilaterale",                   "bilateral"),
  ("ipsilaterale",                 "ipsilateral"),
  ("omolaterale",                  "ipsilateral"),
  ("controlaterale",               "contralateral"),
  ("microscopico",                 "microscopic"),
  ("macroscopico",                 "macroscopic"),
  ("microscopica",                 "microscopic"),
  ("macroscopica",                 "macroscopic"),
  ("microscopicamente",            "microscopically"),
  ("macroscopicamente",            "macroscopically"),
  ("adiacenti",                    "adjacent"),
  ("adiacente",                    "adjacent"),
  ("peritoneale",                  "peritoneal"),
  ("peritoneali",                  "peritoneal"),
  ("mucinoso",                     "mucinous"),
  ("mucinosi",                     "mucinous"),
  ("acellulare",                   "acellular"),
  ("periappendiceal",              "periappendiceal"),
  ("intraperitoneale",             "intraperitoneal"),
  ("intraperitoneali",             "intraperitoneal"),
]

# ════════════════════════════════════════════════════════════════════════════
# 18. N DESCRIPTIONS — common patterns
# ════════════════════════════════════════════════════════════════════════════
N_PATTERNS = [
  ("Linfonodi regionali non valutabili", "Regional lymph nodes not assessable"),
  ("Nessuna metastasi nei linfonodi regionali","No regional lymph node metastasis"),
  ("Nessuna metastasi linfonodale regionale", "No regional lymph node metastasis"),
  ("Metastasi in 1 linfonodo regionale",  "Metastasis in 1 regional lymph node"),
  ("Metastasi in 1-2 linfonodi regionali","Metastasis in 1–2 regional lymph nodes"),
  ("Metastasi in 1–2 linfonodi regionali","Metastasis in 1–2 regional lymph nodes"),
  ("Metastasi in 2-3 linfonodi regionali","Metastasis in 2–3 regional lymph nodes"),
  ("Metastasi in 2–3 linfonodi regionali","Metastasis in 2–3 regional lymph nodes"),
  ("Metastasi in 1-3 linfonodi regionali","Metastasis in 1–3 regional lymph nodes"),
  ("Metastasi in 1–3 linfonodi regionali","Metastasis in 1–3 regional lymph nodes"),
  ("Metastasi in 3-6 linfonodi regionali","Metastasis in 3–6 regional lymph nodes"),
  ("Metastasi in 3–6 linfonodi regionali","Metastasis in 3–6 regional lymph nodes"),
  ("Metastasi in 4-6 linfonodi regionali","Metastasis in 4–6 regional lymph nodes"),
  ("Metastasi in 4–6 linfonodi regionali","Metastasis in 4–6 regional lymph nodes"),
  ("Metastasi in 7 o più linfonodi regionali","Metastasis in 7 or more regional lymph nodes"),
  ("Metastasi in 7-15 linfonodi regionali","Metastasis in 7–15 regional lymph nodes"),
  ("Metastasi in 7–15 linfonodi regionali","Metastasis in 7–15 regional lymph nodes"),
  ("Metastasi in 16 o più linfonodi regionali","Metastasis in 16 or more regional lymph nodes"),
  ("Metastasi in 3 o più linfonodi regionali","Metastasis in 3 or more regional lymph nodes"),
  ("Metastasi in 4 o più linfonodi regionali","Metastasis in 4 or more regional lymph nodes"),
  ("Metastasi in ≥10 linfonodi ascellari omolaterali","Metastasis in ≥10 ipsilateral axillary lymph nodes"),
  ("Metastasi in 4-9 linfonodi ascellari omolaterali","Metastasis in 4–9 ipsilateral axillary lymph nodes"),
  ("Metastasi in 4–9 linfonodi ascellari omolaterali","Metastasis in 4–9 ipsilateral axillary lymph nodes"),
  ("Metastasi in 1-3 linfonodi ascellari omolaterali","Metastasis in 1–3 ipsilateral axillary lymph nodes"),
  ("Metastasi in 1–3 linfonodi ascellari omolaterali","Metastasis in 1–3 ipsilateral axillary lymph nodes"),
  ("Metastasi in un singolo linfonodo ipsilaterale","Metastasis in a single ipsilateral lymph node"),
  ("Metastasi in un singolo linfonodo","Metastasis in a single lymph node"),
  ("Metastasi nei linfonodi inguinali, mesorettali e/o iliaci interni",
   "Metastasis in inguinal, mesorectal and/or internal iliac lymph nodes"),
  ("Metastasi nei linfonodi iliaci esterni","Metastasis in external iliac lymph nodes"),
  ("Metastasi nei linfonodi iliaci esterni E in inguinali/mesorettali/iliaci interni",
   "Metastasis in external iliac lymph nodes AND in inguinal/mesorectal/internal iliac nodes"),
  ("Metastasi nei linfonodi regionali (pelvi vera, sotto la biforcazione delle iliache comuni)",
   "Metastasis in regional lymph nodes (true pelvis, below the common iliac bifurcation)"),
  ("Metastasi nei linfonodi regionali (ilo epatico, arteria epatica propria, vena porta, diaframma inferiore, cava)",
   "Metastasis in regional lymph nodes (hepatic hilum, proper hepatic artery, portal vein, inferior diaphragm, vena cava)"),
  ("Metastasi clinicamente rilevate in linfonodi mammari interni omolaterali",
   "Clinically detected metastasis in ipsilateral internal mammary lymph nodes"),
  ("Metastasi in linfonodi mammari interni omolaterali, non clinicamente rilevati",
   "Metastasis in ipsilateral internal mammary lymph nodes, not clinically detected"),
  ("Metastasi in 1-3 linfonodi ascellari omolaterali (almeno una macrometastasi >2 mm)",
   "Metastasis in 1–3 ipsilateral axillary lymph nodes (at least one macrometastasis >2 mm)"),
  ("Metastasi in linfonodi sopraclaveari omolaterali","Metastasis in ipsilateral supraclavicular lymph nodes"),
  ("Metastasi in linfonodi infraclavicolari omolaterali (livello III)",
   "Metastasis in ipsilateral infraclavicular lymph nodes (level III)"),
  ("Metastasi clinicamente rilevate in linfonodi mammari interni omolaterali in presenza di ≥1 linfonodo ascellare positivo",
   "Clinically detected metastasis in ipsilateral internal mammary lymph nodes with ≥1 positive axillary lymph node"),
  ("con coinvolgimento microscopico dei linfonodi mammari interni (sentinella)",
   "with microscopic involvement of internal mammary lymph nodes (sentinel)"),
  ("senza coinvolgimento ascellare concomitante classificabile come N1a",
   "without concomitant axillary involvement classifiable as N1a"),
  ("Micrometastasi: >0.2 mm e/o >200 cellule, ma ≤2 mm",
   "Micrometastasis: >0.2 mm and/or >200 cells, but ≤2 mm"),
  ("almeno una macrometastasi >2 mm","at least one macrometastasis >2 mm"),
  ("Depositi tumorali (satelliti) nella sottosierosa o nei tessuti pericolici/perirettali non peritonealizzati senza metastasi nei linfonodi regionali",
   "Tumor deposits (satellites) in the subserosa or in the pericolic/perirectal non-peritonealized tissues without regional lymph node metastasis"),
  ("Depositi tumorali (satelliti) nella sottosierosa, nel mesoappendice o nei tessuti periappendicolari non peritonealizzati, senza metastasi nei linfonodi regionali",
   "Tumor deposits (satellites) in the subserosa, mesoappendix or periappendiceal non-peritonealized tissues, without regional lymph node metastasis"),
  ("Metastasi in un singolo linfonodo nella pelvi vera (inguinale o pelvico) ≤2 cm",
   "Metastasis in a single lymph node in the true pelvis (inguinal or pelvic), ≤2 cm"),
  ("Metastasi in un singolo linfonodo >2 cm, o in linfonodi multipli",
   "Metastasis in a single lymph node >2 cm, or in multiple lymph nodes"),
  ("Metastasi in un singolo linfonodo ≤2 cm nella dimensione maggiore",
   "Metastasis in a single lymph node ≤2 cm in greatest dimension"),
  ("Metastasi in un singolo linfonodo >2 cm, o in linfonodi multipli inguinali o pelvici",
   "Metastasis in a single lymph node >2 cm, or in multiple inguinal or pelvic lymph nodes"),
  # Salivary gland N
  ("[pN — V9] Metastasi in 1–3 linfonodi regionali, pENE assente",
   "[pN — V9] Metastasis in 1–3 regional lymph nodes, pENE absent"),
  ("[pN — V9] Metastasi in 1–3 linfonodi con pENE presente (trasgressione capsula nel tessuto adiposo), OPPURE metastasi in ≥4 linfonodi (qualsiasi stato pENE). Nota: pN3 eliminato in UICC/AJCC Version 9.",
   "[pN — V9] Metastasis in 1–3 lymph nodes with pENE present (capsular transgression into adipose tissue), OR metastasis in ≥4 lymph nodes (any pENE status). Note: pN3 eliminated in UICC/AJCC Version 9."),
  ("[cN] Metastasi in un singolo linfonodo ipsilaterale ≤3 cm, ENE clinica assente",
   "[cN] Metastasis in a single ipsilateral lymph node ≤3 cm, clinical ENE absent"),
  ("[cN] Metastasi in un singolo linfonodo ipsilaterale >3 cm e ≤6 cm, ENE clinica assente",
   "[cN] Metastasis in a single ipsilateral lymph node >3 cm and ≤6 cm, clinical ENE absent"),
  ("[cN] Metastasi in linfonodi multipli ipsilaterali ≤6 cm, ENE clinica assente",
   "[cN] Metastasis in multiple ipsilateral lymph nodes ≤6 cm, clinical ENE absent"),
  ("[cN] Metastasi in linfonodi bilaterali o controlaterali ≤6 cm, ENE clinica assente",
   "[cN] Metastasis in bilateral or contralateral lymph nodes ≤6 cm, clinical ENE absent"),
  ("[cN] Metastasi in linfonodo >6 cm, ENE clinica assente",
   "[cN] Metastasis in lymph node >6 cm, clinical ENE absent"),
  ("[cN] Metastasi in qualsiasi linfonodo con ENE clinica conclamata (fissità, invasione strutture adiacenti, deficit nervo cranico, edema cutaneo)",
   "[cN] Metastasis in any lymph node with overt clinical ENE (fixation, invasion of adjacent structures, cranial nerve deficit, skin edema)"),
  # Testis N
  ("Metastasi nei linfonodi retroperitoneali","Metastasis in retroperitoneal lymph nodes"),
  # Common terms
  ("linfonodi regionali",          "regional lymph nodes"),
  ("linfonodi ascellari",          "axillary lymph nodes"),
  ("linfonodo sentinella",         "sentinel lymph node"),
  ("linfonodo",                    "lymph node"),
  ("linfonodi",                    "lymph nodes"),
  ("senza metastasi nei linfonodi regionali","without regional lymph node metastasis"),
  ("non clinicamente rilevati",    "not clinically detected"),
  ("clinicamente rilevati",        "clinically detected"),
  ("biopsia del linfonodo sentinella","sentinel lymph node biopsy"),
  ("biopsia del sentinella",       "sentinel biopsy"),
  ("pENE assente",                 "pENE absent"),
  ("pENE presente",                "pENE present"),
  ("ENE clinica assente",          "clinical ENE absent"),
  ("ENE clinica conclamata",       "overt clinical ENE"),
]

# ════════════════════════════════════════════════════════════════════════════
# 19. M DESCRIPTIONS — common patterns
# ════════════════════════════════════════════════════════════════════════════
M_PATTERNS = [
  ("Nessuna metastasi a distanza (include citologia peritoneale negativa)",
   "No distant metastasis (including negative peritoneal cytology)"),
  ("Nessuna metastasi a distanza clinicamente o radiologicamente evidenti",
   "No distant metastasis clinically or radiologically evident"),
  ("Nessuna metastasi a distanza clinicamente o radiologicamente evidenti; nessuna evidenza di metastasi alla PET",
   "No distant metastasis clinically or radiologically evident; no evidence of metastasis on PET"),
  ("Nessuna metastasi a distanza",  "No distant metastasis"),
  ("Metastasi confinate a un singolo organo (fegato, polmone, ovaio, linfonodi non regionali), senza metastasi peritoneali",
   "Metastasis confined to a single organ (liver, lung, ovary, non-regional lymph nodes), without peritoneal metastasis"),
  ("Metastasi in più di un organo", "Metastasis in more than one organ"),
  ("Metastasi al peritoneo, con o senza coinvolgimento di altri organi",
   "Peritoneal metastasis, with or without involvement of other organs"),
  ("Metastasi a distanza (include semina peritoneale, citologia positiva, metastasi omentali)",
   "Distant metastasis (including peritoneal seeding, positive cytology, omental metastases)"),
  ("Metastasi a distanza rilevate clinicamente o radiologicamente",
   "Distant metastasis detected clinically or radiologically"),
  ("Metastasi a distanza confermate istologicamente (qualsiasi sede)",
   "Distant metastasis confirmed histologically (any site)"),
  ("Metastasi a distanza confirmate istologicamente",
   "Distant metastasis confirmed histologically"),
  ("Metastasi a distanza",          "Distant metastasis"),
  # Appendix M
  ("Solo mucina acellulare intraperitoneale",
   "Acellular intraperitoneal mucin only"),
  ("Metastasi intraperitoneale con epitelio mucinoso (grado determina IVA vs IVB)",
   "Intraperitoneal metastasis with mucinous epithelium (grade determines IVA vs IVB)"),
  ("Metastasi non peritoneali",     "Non-peritoneal metastasis"),
  # Testis M
  ("Metastasi linfonodali retroperitoneali, nessuna metastasi viscerale non linfonodale",
   "Retroperitoneal lymph node metastasis, no non-lymph node visceral metastasis"),
  # Thyroid M
  ("Metastasi a distanza (all'eccezione dei linfonodi del collo):",
   "Distant metastasis (except neck lymph nodes):"),
  # cM0(i+)
  ("Nessuna metastasi clinica o radiologica, ma cellule tumorali isolate rilevate nel sangue, midollo osseo o tessuti non regionali (≤0.2 mm) in assenza di sintomi o segni. Non modifica lo stadio M (rimane M0)",
   "No clinical or radiological metastasis, but isolated tumor cells detected in blood, bone marrow or non-regional tissues (≤0.2 mm) in the absence of symptoms or signs. Does not modify M stage (remains M0)"),
  # Small intestine M
  ("Metastasi a distanza clinicamente o radiologicamente evidenti",
   "Distant metastasis clinically or radiologically evident"),
  ("Metastasi a distanza confermate istologicamente",
   "Distant metastasis confirmed histologically"),
  # Melanoma M subtypes
  ("Metastasi nella cute, nei tessuti molli compresi i muscoli e/o nei linfonodi non regionali",
   "Metastasis in the skin, soft tissues including muscles and/or non-regional lymph nodes"),
  ("Metastasi nel polmone con o senza coinvolgimento delle sedi M1a",
   "Metastasis in the lung with or without M1a site involvement"),
  ("Metastasi in organi non polmonari viscerali con o senza coinvolgimento di M1a o M1b",
   "Metastasis in non-pulmonary visceral organs with or without M1a or M1b involvement"),
  ("Metastasi nel sistema nervoso centrale con o senza coinvolgimento di altre sedi",
   "Metastasis in the central nervous system with or without involvement of other sites"),
]

for it, en in T_PATTERNS + N_PATTERNS + M_PATTERNS:
    txt = txt.replace(it, en)

# ════════════════════════════════════════════════════════════════════════════
# 20. SITE NOTES (note: field) — translated in full
# These are the complex clinical paragraphs; replace each entirely
# ════════════════════════════════════════════════════════════════════════════
NOTE_TRANSLATIONS = {
# Colon & rectum
"≥12 linfonodi per pN0 adeguato. TD (depositi tumorali) classificati come N1c se LN negativi. OGJ con epicentro >2 cm dal GEJ → staging gastrico.":
"≥12 lymph nodes for adequate pN0. TD (tumor deposits) classified as N1c if LN negative. OGJ with epicenter >2 cm from GEJ → gastric staging.",

"≥16 linfonodi per pN0 adeguato. Epicentro OGJ ≤2 cm dalla GEJ (Siewert I/II) → staging esofageo.":
"≥16 lymph nodes for adequate pN0. OGJ epicenter ≤2 cm from GEJ (Siewert I/II) → esophageal staging.",

"≥7 linfonodi per pN0 adeguato. GEJ con epicentro ≤2 cm → staging esofageo. Stage Group anatomico separato per SCC e Adeno (clinico e patologico). I Pathological Prognostic Groups con grado e sede non sono implementati nel motore di calcolo.":
"≥7 lymph nodes for adequate pN0. GEJ with epicenter ≤2 cm → esophageal staging. Separate anatomic Stage Group for SCC and Adeno (clinical and pathological). Pathological Prognostic Groups with grade and location are not implemented in this tool.",

"≥6 linfonodi per pN0. Esclude l'ampolla di Vater.":
"≥6 lymph nodes for adequate pN0. Excludes the ampulla of Vater.",

"AJCC Version 9 / UICC V9 ≥12 linfonodi per pN0. Comprende adenocarcinomi (mucinosi e non) e NEC scarsamente differenziati. NET ben differenziati: classificazione separata. V9: HAMN (High-grade Appendiceal Mucinous Neoplasm) aggiunto accanto a LAMN; adenocarcinoma a cellule goblet (ex goblet cell carcinoide — terminologia abbandonata in V9). M1a: solo mucina acellulare intraperitoneale; M1b: epitelio mucinoso intraperitoneale (il grado determina IVA vs IVB); M1c: metastasi non peritoneali.":
"AJCC Version 9 / UICC V9 ≥12 lymph nodes for adequate pN0. Includes adenocarcinomas (mucinous and non-mucinous) and poorly differentiated NECs. Well-differentiated NETs: separate classification. V9: HAMN (High-grade Appendiceal Mucinous Neoplasm) added alongside LAMN; goblet cell adenocarcinoma (formerly goblet cell carcinoid — terminology abandoned in V9). M1a: acellular intraperitoneal mucin only; M1b: intraperitoneal mucinous epithelium (grade determines IVA vs IVB); M1c: non-peritoneal metastasis.",

"⚠ Tis e Stadio 0 deliberatamente ESCLUSI seguendo AJCC Cancer Staging Manual Version 9: HSIL/AIN II-III non è un carcinoma invasivo; la sua inclusione nello staging TNM portava a overtreatment. Evidenza: studio ANCHOR e analisi SEER. UICC V9 2025 mantiene invece Tis/Stadio 0 per uniformità registrale — divergenza UICC/AJCC esplicita. Scelta del tool: AJCC v9 (clinicamente più solida). Schema si applica a SCC del canale anale; i carcinomi del margine anale (cute perianale entro 5 cm) seguono lo staging cutaneo (carcinoma_cute). HPV status: fattore prognostico raccomandato da AJCC, non incluso nello staging. ≥12 linfonodi per pN peri-rettale/pelvico; ≥6 per pN inguinale.":
"⚠ Tis and Stage 0 deliberately EXCLUDED following AJCC Cancer Staging Manual Version 9: HSIL/AIN II-III is not invasive carcinoma; its inclusion in TNM staging led to overtreatment. Evidence: ANCHOR trial and SEER analysis. UICC V9 2025 retains Tis/Stage 0 for registry uniformity — explicit UICC/AJCC divergence. Tool choice: AJCC v9 (clinically more robust). Schema applies to SCC of the anal canal; carcinomas of the anal margin (perianal skin within 5 cm) follow cutaneous staging (skin_carcinoma). HPV status: prognostic factor recommended by AJCC, not included in staging. ≥12 lymph nodes for perirectal/pelvic pN; ≥6 for inguinal pN.",

"Solo per epatocarcinoma (HCC). CCA e HCC-CC misto hanno classificazione separata (Dotti biliari intraepatici). ≥3 linfonodi per pN0. Il BCLC (Barcelona Clinic Liver Cancer stage) è sistema prognostico parallelo frequentemente usato in clinica.":
"For hepatocellular carcinoma (HCC) only. CCA and mixed HCC-CC have a separate classification (Intrahepatic bile ducts). ≥3 lymph nodes for adequate pN0. The BCLC (Barcelona Clinic Liver Cancer stage) is a parallel prognostic system frequently used in clinical practice.",

"⚠ Staging prostata: raggruppamento anatomico T/N/M — il gruppo prognostico formale richiede anche PSA e Grade Group (Gleason score), non implementati in questo motore. Esclusi i carcinomi uroteliali della prostata (staging ureterale). Nessun pT1. Suffix MRI: (mr); PSMA-PET: (PET) da indicare in referto.":
"⚠ Prostate staging: anatomic T/N/M grouping — the formal prognostic group also requires PSA and Grade Group (Gleason score), not implemented in this tool. Urothelial carcinomas of the prostate excluded (ureteral staging). No pT1. MRI suffix: (mr); PSMA-PET: (PET) to be indicated in the report.",

"Esclude papilloma e PUNLMP. Suffisso (m): tumori multipli; suffisso (is): CIS associato. Staging corrisponde sia a c che pTNM.":
"Excludes papilloma and PUNLMP. Suffix (m): multiple tumors; suffix (is): associated CIS. Staging applies to both c and pTNM.",

"≥6 linfonodi per pN0 (livello I ascellare). pN basato sul componente invasivo; il DCIS non conta ai fini della classificazione N. ITC (≤0.2 mm o ≤200 cellule) = N0(i+): non modificano lo stadio. Distinguere sempre cN (clinico/imaging) da pN (patologico): cN1 ≠ pN1 per implicazioni terapeutiche. Includere sempre il modificatore (sn) se la classificazione N deriva dal solo sentinella. AJCC esclude Tis(LCIS). ⚠ Staging mostrato: solo raggruppamento anatomico UICC (T/N/M). I Prognostic Stage Groups AJCC (con recettori ormonali, HER2, Ki67, grading) NON sono implementati.":
"≥6 lymph nodes for adequate pN0 (axillary level I). pN based on the invasive component; DCIS does not count for N classification. ITC (≤0.2 mm or ≤200 cells) = N0(i+): do not modify stage. Always distinguish cN (clinical/imaging) from pN (pathological): cN1 ≠ pN1 for therapeutic implications. Always include the (sn) modifier if N classification derives from sentinel node only. AJCC excludes Tis(LCIS). ⚠ Stage shown: UICC anatomic grouping only (T/N/M). AJCC Prognostic Stage Groups (with hormone receptors, HER2, Ki67, grade) are NOT implemented.",

"AJCC Version 9 / UICC V9: pN semplificato (numerica + pENE); cN mantiene schema dimensionale completo con N3. Ghiandole maggiori (parotide, sottomandibolare, sottolinguale). Minimo LN: ≥10 (neck selettiva) o ≥15 (radicale) per pN0 adeguato. ENE (Extranodal Extension) — definizioni: cENE (clinica) = fissità linfonodale, invasione strutture adiacenti, deficit nervo cranico, edema cutaneo su linfonodo; pENE (patologica) = trasgressione istologica attraverso l'intera capsula linfonodale nel tessuto adiposo circostante (esclude semplice assottigliamento capsulare). pENE trasforma pN1→pN2. Discordanza cN/pN frequente: un linfonodo controlaterale singolo pENE- è pN1 (numerica) ma era cN2c (clinica pre-op). pN3 ELIMINATO in V9. cN3a (>6 cm) e cN3b (ENE clinica) → entrambi Stadio IVA.":
"AJCC Version 9 / UICC V9: simplified pN (numeric + pENE); cN retains the full dimensional schema with N3. Major glands (parotid, submandibular, sublingual). Minimum LN: ≥10 (selective neck) or ≥15 (radical) for adequate pN0. ENE (Extranodal Extension) — definitions: cENE (clinical) = lymph node fixation, invasion of adjacent structures, cranial nerve deficit, skin edema over lymph node; pENE (pathological) = histological transgression through the entire lymph node capsule into the surrounding adipose tissue (excludes simple capsular thinning). pENE upgrades pN1→pN2. Frequent cN/pN discordance: a single contralateral pENE− lymph node is pN1 (numeric) but was cN2c (pre-op clinical). pN3 ELIMINATED in V9. cN3a (>6 cm) and cN3b (clinical ENE) → both Stage IVA.",
}

for it_note, en_note in NOTE_TRANSLATIONS.items():
    txt = txt.replace(it_note, en_note)

# ════════════════════════════════════════════════════════════════════════════
# 21. AJCC_NOTES content (keep mostly in English since they reference standards,
#     but translate Italian meta-commentary)
# ════════════════════════════════════════════════════════════════════════════
R += [
  # Mammella AJCC notes
  ("'UICC include Tis(LCIS) nello Stadio 0. AJCC Cancer Staging Manual, Version 9: Tis(LCIS) ESCLUSA — non classificabile secondo AJCC.'",
   "'UICC includes Tis(LCIS) in Stage 0. AJCC Cancer Staging Manual, Version 9: Tis(LCIS) EXCLUDED — not classifiable per AJCC.'"),
  ("'Mammella: UICC e AJCC identici eccetto Tis(LCIS) → Stadio 0 solo per UICC.'",
   "'Breast: UICC and AJCC identical except Tis(LCIS) → Stage 0 only for UICC.'"),
  # Prostata
  ("'⚠ AJCC Cancer Staging Manual, Version 9 NON usa il raggruppamento anatomico T/N/M per la prostata nella pratica clinica. Usa i Prognostic Stage Groups che richiedono PSA (ng/mL) e Grade Group (1–5, da Gleason score). Lo stadio anatomico mostrato qui è UICC; per AJCC integrare PSA e GG.'",
   "'⚠ AJCC Cancer Staging Manual, Version 9 does NOT use anatomic T/N/M grouping for prostate in clinical practice. It uses Prognostic Stage Groups requiring PSA (ng/mL) and Grade Group (1–5, from Gleason score). The anatomic stage shown here is UICC; for AJCC, integrate PSA and GG.'"),
  # Esofago
  ("'⚠ AJCC Cancer Staging Manual, Version 9: Pathological Prognostic Groups per SCC e Adeno includono grado istologico e sede anatomica del tumore — possono differire di 1 stadio rispetto allo Stage Group anatomico UICC per lo stesso T/N/M. Il motore implementa solo lo Stage Group anatomico (UICC). Per staging AJCC completo consultare la fonte primaria.'",
   "'⚠ AJCC Cancer Staging Manual, Version 9: Pathological Prognostic Groups for SCC and Adeno include histological grade and tumor anatomic location — may differ by 1 stage from the UICC anatomic Stage Group for the same T/N/M. This tool implements only the anatomic Stage Group (UICC). For complete AJCC staging, consult the primary source.'"),
  # Gh salivari
  ("'AJCC Version 9 / UICC V9: classificazione N radicalmente rivista. pN3 ELIMINATO. N ora basato su numero LN e pENE (non dimensione o lateralità). Downgrading complessivo: casi precedentemente IVA/IVB per N2/N3 dimensionale ora classificati come Stadio III. Stadio IV riservato esclusivamente a M1.'",
   "'AJCC Version 9 / UICC V9: N classification radically revised. pN3 ELIMINATED. N now based on LN number and pENE (not size or laterality). Overall downgrading: previously IVA/IVB cases by dimensional N2/N3 now classified as Stage III. Stage IV exclusively reserved for M1.'"),
  # Melanoma
  ("'AJCC Cancer Staging Manual, Version 9: aggiunge suffisso LDH alle sottocategorie M — M1a(0)/M1a(1), M1b(0)/M1b(1), M1c(0)/M1c(1), M1d(0)/M1d(1) — dove (0)=LDH normale, (1)=LDH elevata. UICC V9 non adotta formalmente il suffisso LDH. Staging T/N/M e Stage Groups: identici.'",
   "'AJCC Cancer Staging Manual, Version 9: adds LDH suffix to M subcategories — M1a(0)/M1a(1), M1b(0)/M1b(1), M1c(0)/M1c(1), M1d(0)/M1d(1) — where (0)=normal LDH, (1)=elevated LDH. UICC V9 does not formally adopt the LDH suffix. T/N/M staging and Stage Groups: identical.'"),
  # Canale anale AJCC badge text
  ("badges:[{cls:'badge-div',txt:'AJCC v9: Tis/Stadio 0 esclusi'}]",
   "badges:[{cls:'badge-div',txt:'AJCC v9: Tis/Stage 0 excluded'}]"),
  # Mammella badges
  ("badges:[{cls:'badge-div',txt:'UICC≠AJCC (LCIS)'}]",
   "badges:[{cls:'badge-div',txt:'UICC≠AJCC (LCIS)'}]"),
  # Esofago model limited badge
  ("badges:[{cls:'badge-partial',txt:'PPG con grado/sede non implementati'}]",
   "badges:[{cls:'badge-partial',txt:'PPG with grade/location not implemented'}]"),
  # Prostata model limited badge
  ("badges:[{cls:'badge-anat',txt:'Anatomico'}]",
   "badges:[{cls:'badge-anat',txt:'Anatomic'}]"),
]

# ════════════════════════════════════════════════════════════════════════════
# 22. Remaining Italian coverage notes in SITES
# ════════════════════════════════════════════════════════════════════════════
R += [
  # Various note fields not caught above
  ("note:'≥12 linfonodi per pN0. Esclude sedi diverse dal dotto biliare comune distale.",
   "note:'≥12 lymph nodes for adequate pN0. Excludes sites other than the distal common bile duct."),
  ("note:'≥6 linfonodi per pN0. Klatskin (Bismuth) — biliari periilari.",
   "note:'≥6 lymph nodes for adequate pN0. Klatskin (Bismuth) — perihilar bile ducts."),
  ("Stadio anatomico — separato da HCC.",     "Anatomic stage — separate from HCC."),
  ("Esclude i carcinomi uroteliali",           "Excludes urothelial carcinomas"),
  ("classificazione separata",                 "separate classification"),
  ("Esclude papilloma e PUNLMP",               "Excludes papilloma and PUNLMP"),
  ("Suffisso (m): tumori multipli",            "Suffix (m): multiple tumors"),
  ("suffisso (is): CIS associato",             "suffix (is): associated CIS"),
  ("corrisponde sia a c che pTNM",             "applies to both c and pTNM"),
  ("nota separata",                            "separate note"),
  ("Minimo LN", "Minimum LN"),
  ("non sono implementati nel motore di calcolo", "are not implemented in the calculation engine"),
  ("non sono implementati in questo motore", "are not implemented in this tool"),
  ("non implementati in questo motore", "not implemented in this tool"),
  # Misc remaining Italian
  ("Sede", "Site"),
  ("sedi", "sites"),
  ("sede", "site"),
  ("Tumori", "Tumors"),
  ("tumore", "tumor"),
  ("Tumore", "Tumor"),
  ("ben differenziati", "well-differentiated"),
  ("scarsamente differenziati", "poorly differentiated"),
  ("grado istologico", "histological grade"),
  ("marcatori sierici", "serum markers"),
  ("nadir post-orchidectomia", "post-orchiectomy nadir"),
  ("fattore prognostico", "prognostic factor"),
  ("fattori prognostici", "prognostic factors"),
  ("uso clinico", "clinical use"),
  ("fonte primaria", "primary source"),
  ("classificazione separata", "separate classification"),
  # ── Mammella AJCC v9 PSG translations ─────────────────────────────────────
  ('Stadio anatomico UICC + Prognostic Stage Group AJCC v9', 'UICC V9 anatomic stage + AJCC 8th ed. Prognostic Stage Group'),
  ("txt:'PSG AJCC v9'", "txt:'AJCC 8th ed. PSG'"),
  ("label:'HER2 ISH/FISH (se IHC 2+)'", "label:'HER2 ISH/FISH (if IHC 2+)'"),
  ("label:'Grado Nottingham'", "label:'Nottingham grade'"),
  ("placeholder:'es. 25'", "placeholder:'e.g. 25'"),
  ("'Amplificato (ratio ≥2.0 o ≥6 copie)'", "'Amplified (ratio ≥2.0 or ≥6 copies)'"),
  ("'Non amplificato'", "'Non-amplified'"),
  ('── PROFILO BIOMARCATORI (ASCO/CAP 2023) ──────────────', '── BIOMARKER PROFILE (ASCO/CAP 2023) ───────────────'),
  ('HER2 categoria: ', 'HER2 category: '),
  ('Grado Nottingham: ', 'Nottingham grade: '),
  ('── STADIO PROGNOSTICO AJCC v9 ─────────────────────────', '── AJCC 8th ed. PROGNOSTIC STAGE ─────────────────────────'),
  ("'\\nDeterminanti: '", "'\\nDeterminants: '"),
  ('\\n⚠ Verificare con: AJCC Cancer Staging Manual, Version 9', '\\n⚠ Verify with: AJCC Cancer Staging Manual, 8th Edition (2017)'),
  ('Prognostic Stage Group: non calcolabile — dati mancanti (', 'Prognostic Stage Group: not calculable — missing data ('),
  ('Prognostic Stage Group AJCC v9 non calcolabile — biomarcatori mancanti: ', 'AJCC 8th ed. Prognostic Stage Group not calculable — missing biomarkers: '),
  ('ISH/FISH non documentato. Aggiungere risultato ISH per classificazione HER2-low vs HER2-positivo.', 'ISH/FISH not documented. Add ISH result to classify HER2-low vs HER2-positive.'),
  ("'HER2-positivo (IHC 3+)'", "'HER2-positive (IHC 3+)'"),
  ("'HER2-positivo (IHC 2+/ISH amplificato)'", "'HER2-positive (IHC 2+/ISH amplified)'"),
  ("'HER2-low (IHC 2+/ISH non amplificato)'", "'HER2-low (IHC 2+/ISH non-amplified)'"),
  ("'HER2 equivoco (IHC 2+ — ISH pendente)'", "'HER2 equivocal (IHC 2+ — ISH pending)'"),
  ('Prognostic Stage Group AJCC v9 implementato: compilare ER, PR, HER2 IHC (±ISH se IHC 2+), Grado Nottingham nel pannello Biomarcatori (scheda Referto). HER2-low (IHC 1+ o IHC 2+/ISH−): rilevante per T-DXd (DESTINY-Breast04, NEJM 2022).', 'AJCC 8th ed. Prognostic Stage Group implemented: fill in ER, PR, HER2 IHC (±ISH if IHC 2+), Nottingham grade in the Biomarker panel (Report tab). HER2-low (IHC 1+ or IHC 2+/ISH−): relevant for T-DXd (DESTINY-Breast04, NEJM 2022).'),
  ('Prognostic Stage Group AJCC v9: richiede ER, PR, HER2 (IHC + ISH se 2+), Grado Nottingham. HER2-low (IHC 1+ o IHC 2+/ISH−) riportato nel referto. Verificare con AJCC Cancer Staging Manual v9.', 'AJCC 8th ed. Prognostic Stage Group: requires ER, PR, HER2 (IHC + ISH if 2+), Nottingham grade. HER2-low (IHC 1+ or IHC 2+/ISH−) reported in the pathology report. Verify with AJCC Cancer Staging Manual v9.'),
  ('Mammella: Prognostic Stage Group', 'Breast: Prognostic Stage Group'),
  ('Mammella: HER2 IHC 2+', 'Breast: HER2 IHC 2+'),
  ('se IHC 2+', 'if IHC 2+'),  ('Mammella: AJCC v9 Prognostic Stage Group', 'Breast: AJCC 8th ed. Prognostic Stage Group'),

]

# ════════════════════════════════════════════════════════════════════════════
# 23. Apply ALL replacements
# ════════════════════════════════════════════════════════════════════════════
for it, en in R:
    txt = txt.replace(it, en)

with open(DST, 'w', encoding='utf-8') as f:
    f.write(txt)

print(f"Done. Written to {DST}")
