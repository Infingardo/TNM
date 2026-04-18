# TNM 9ª Edizione — Tool per Anatomia Patologica

Strumento HTML/JS autonomo per la classificazione TNM dei tumori maligni secondo la **9ª edizione UICC (2025)**, con mapping AJCC v9 per sede dove applicabile e verificato.

> *"Tu non stai automatizzando la diagnosi. Stai automatizzando la prudenza."*

---

## Caratteristiche principali

### Tre modalità integrate
| Tab | Funzione |
|-----|----------|
| **📋 Definizioni** | Lookup rapido di tutte le categorie T, N, M con descrizione completa in italiano |
| **🎯 Stadiazione** | Calcolo interattivo dello stadio con validazione in tempo reale |
| **📄 Referto** | Generazione di testo strutturato pronto per il LIS / copia-incolla |

### Sedi coperte (26 totali)

**Apparato digerente**
Colon e Retto · Stomaco · Esofago/GEJ · Intestino Tenue · Appendice · Canale Anale · Fegato (HCC) · Dotti biliari intraepatici (CCA) · Dotti biliari peribiliari (Klatskin) · Via biliare distale · Colecisti · Ampolla di Vater · Pancreas (adenocarcinoma)

**NET Gastrointestinali** (WHO 2022, AJCC 9ª)
NET GI — Stomaco · NET GI — Colon-Retto · NET GI — Pancreas

**Testa e Collo**
Tiroide (4 varianti: PTC/FTC <55aa, PTC/FTC ≥55aa, midollare, anaplastico) · Ghiandole salivari

**Mammella · Urologico**
Mammella · Prostata · Vescica · Rene (RCC) · Testicolo (con marcatori S)

**Cute / Melanoma**
Melanoma cutaneo (staging clinico e patologico) · Carcinoma della cute (SCC/BCC) · Carcinoma di Merkel

---

## Funzionalità del motore

### Stadiazione
- Gerarchia T/N/M: `T1a` matcha regole `T1`, `N2b` matcha regole `N2`, ecc.
- Varianti per sede: staging clinico vs patologico (Stomaco, Esofago SCC/Adeno, Prostata), per età (Tiroide), per istotipo (Melanoma, Merkel)
- Categorie speciali autonome: **N1mi** e **N1a(sn)** non vengono assorbite dalla gerarchia N1 (evita overstaging mammella/Merkel)
- Campi extra obbligatori: grado istologico per Appendice (M1b → IVA vs IVB), marcatori S per Testicolo
- Ambiguità dataset → `stage: null` (mai lo stadio più alto di default)

### Validazione in tempo reale
| Tipo | Esempi |
|------|--------|
| **Errore bloccante** | pM0 (non esiste), N0 + LN positivi, N1c + LN+ in colon/appendice, cT+pN chimera, LN positivi > totale |
| **Dato incompleto** | M1b appendice senza grado, staging fuori modello |
| **Warning clinico** | pN0 con campionamento sotto soglia (sede-specifico), S=SX testicolo, variante/prefisso incoerente, staging anatomico prostata |

### Prefissi separati T/N/M
- Select indipendenti per T, N, M (es. `ypT` `ypN` `cM` — tipico post-neoadiuvante)
- Preset: `pTNM (p/p/c)`, `pTNM (p/p/p)`, `cTNM`, `ypTNM`, `ycTNM`, `rTNM`
- Staging ibrido fisiologico (p/p/c, yp/yp/c, r/r/c) — nessun falso allarme
- Chimera cT+pN → errore bloccante

### Auto-calcolo N da LN positivi
Per le sedi con N numerico puro, inserendo il numero di linfonodi positivi il campo N si compila automaticamente:

| Sede | Logica |
|------|--------|
| Colon-Retto | 0→N0, 1→N1a, 2-3→N1b, 4-6→N2a, ≥7→N2b |
| Stomaco | 0→N0, 1-2→N1, 3-6→N2, 7-15→N3a, ≥16→N3b |
| Esofago | 0→N0, 1-2→N1, 3-6→N2, ≥7→N3 |
| Pancreas / Ampolla / Vie biliari | 0→N0, 1-3→N1, ≥4→N2 |
| Appendice | 0→N0, 1→N1a, 2-3→N1b, ≥4→N2 |
| Mammella | 0→N0, 1-3→N1a, 4-9→N2a, ≥10→N3a |

> N1c (depositi tumorali), N1mi (micrometastasi), N1a(sn) (sentinella) richiedono valutazione morfologica — non auto-calcolabili.

### Referto strutturato
- Riga compatta LIS-ready: `━━ pT3 pN1a (3/24) cM0 → Stadio IIIB`
- Rapporto linfonodi integrato nel campo N: `pN1a (3/24)`
- 4 stati di qualità: `assegnato` / `assegnato con riserva` / `non assegnabile — incompleto` / `non assegnabile — incoerente`
- Label separata per modelli ridotti: `RAGGRUPPAMENTO ANATOMICO TNM` (prostata, esofago)
- Fattori prognostici non-TNM opzionali:
  - LVI (presente / non identificata nel campione / non valutabile)
  - PNI (idem)
  - Budding tumorale ITBCC 2016 — solo per sedi pertinenti (colon-retto, appendice, intestino tenue, stomaco, esofago)
  - Margini di resezione (R0/R1/R2/RX)
  - Regressione post-neoadiuvante (Ryan 0-3 con descrizione morfologica)
  - Perforazione

### Sincronizzazione tra tab
- I dati inseriti nel tab Stadiazione (T/N/M, LN, prefissi, variante, extra) si propagano automaticamente al tab Referto
- Nessuna reinserzione necessaria tra i due tab
- **Stadiazione è la sorgente di verità**: le modifiche nel tab Referto rimangono locali

---

## Limitazioni dichiarate

| Sede | Limitazione |
|------|-------------|
| Prostata | Raggruppamento anatomico T/N/M — il **Prognostic Stage Group formale richiede PSA + Grade Group (Gleason)**. Esplicitato nell'output. |
| Esofago | Staging anatomico — i **Pathological Prognostic Groups con grado e sede** (AJCC) non sono implementati. |
| Testicolo S=SX | Stadio I generico senza sottostadio (IA/IB/IS) — richiede nadir AFP/hCG/LDH. |
| UICC vs AJCC | Divergenze dichiarate per sede (es. mammella Tis(LCIS): UICC sì, AJCC no; tiroide: alcune varianti). |
| Sedi non incluse | Faringe, Laringe, Cavo orale, Pelvi renale/uretere, Sedi ginecologiche, Linfomi, SNC. |

---

## Utilizzo

Nessuna installazione, nessuna connessione a internet. Il tool è un singolo file HTML autonomo (~115 KB):

```
TNM_9ed_Tool.html  →  aprire in qualsiasi browser moderno
```

**Flusso tipico**
1. Seleziona la sede dal pannello sinistro (o usa la barra di ricerca)
2. Tab **Definizioni** — verifica le categorie T/N/M prima di classificare
3. Tab **Stadiazione** — inserisci LN esaminati/positivi → N si auto-suggerisce; seleziona T, N, M; calcola
4. Tab **Referto** — aggiungi fattori prognostici opzionali; genera e copia
5. **🆕 Nuovo caso** per azzerare tutti i campi

---

## Architettura tecnica

```
TNM_9ed_Tool.html
├── CSS (theme off-white, badge, validation colors)
├── HTML (sidebar · topbar · 3 tab panels)
└── JS (~1800 righe, no dipendenze esterne)
    ├── PARENTS{}         Gerarchia T/N/M (parent-child matching)
    ├── SITES[]           Dataset 26 sedi con T/N/M definitions + staging rules
    ├── N_AUTO_RULES{}    Auto-calcolo N da LN+ per sede
    ├── stripPfx()        Stripping prefisso esplicito (yp|yc|rp|p|c|r|y)
    ├── codeMatch()       Matching con gerarchia PARENTS
    ├── computeBestStage() → {stage, ambiguous, allStages}
    │   └── ambiguity: distinctStages.length>1 → stage:null (mai upstaging silenzioso)
    ├── validateCase()    Validazione centralizzata → {errors, incomplete, warnings, isHybrid}
    ├── renderValidation() Box colorati per tipo (errore/incompleto/warning/ibrido)
    └── sync*()           Sincronizzazione unidirezionale Stadiazione→Referto
```

### Principi di design del motore
- **Ambiguità blocca, non risolve** — se due stadi diversi matchano, `stage: null`
- **Validazione precede lo staging** — gli errori bloccanti impediscono il calcolo
- **N1mi e N1a(sn) sono categorie autonome** — escluse dalla gerarchia N1 per evitare overstaging
- **pN0 adequacy** gated sul prefisso patologico (p/yp/r) — nessun falso allarme su cN0
- **N1c site-specific** — errore solo nelle sedi con semantica "tumor deposits" (colon, appendice), non nel canale anale
- **pM0 non esiste** — errore bloccante

### Test suite
Il motore è coperto da **58 test funzionali** eseguibili in Node.js (no framework) che coprono: stadiazione di 8 sedi, gerarchia T/N/M, prefissi, ibrido severity, validazioni, integrità dataset.

---

## Riferimenti

- **UICC TNM Classification of Malignant Tumours, 9ª Edizione** — Brierley, Giuliani, O'Sullivan, Rous, Van Eycken (eds.) — John Wiley & Sons, 2025
- **AJCC Cancer Staging Manual, Version 9** — dove applicabile e verificato per sede
- **WHO Classification of Tumours** (5ª ed., varie sedi) — per grading NET GI
- **ITBCC 2016** — per grading budding tumorale

> Questo tool è sviluppato per uso esclusivo in anatomia patologica da personale medico qualificato. Non sostituisce la valutazione clinico-patologica né la consultazione della fonte primaria. UICC e AJCC divergono in alcune sedi — verificare per sede.

---

## Sviluppo

Tool sviluppato con metodologia di **revisione multi-sistema**: sviluppo iterativo con Claude (Anthropic) e revisione editoriale/critica incrociata con ChatGPT (OpenAI). Le revisioni critiche hanno guidato correzioni successive del motore, della validazione e dell'architettura del dataset.

Segnalare bug o divergenze con la fonte primaria aprendo una Issue con: sede, combinazione T/N/M, stadio atteso vs stadio ottenuto.

---

*Filippo Maria Domenico Bianchi — SC Anatomia Patologica, ASST Fatebenefratelli-Sacco, Milano*
